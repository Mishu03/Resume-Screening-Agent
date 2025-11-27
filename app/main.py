# app/main.py
import streamlit as st
from resume_parser import extract_text_from_file
from jd_parser import clean_jd_text
from embedding_engine import compute_embeddings, normalize_embeddings, get_model
from matcher import rank_resumes_by_jd
from explanation import explain_candidate
from database import init_db, create_run, save_candidate, get_runs, get_candidates_for_run
import pandas as pd
import os

st.set_page_config(page_title="Resume Screening Agent — Free", layout="wide")
st.title("Resume Screening Agent")

st.markdown(
    "Upload a Job Description and multiple resumes (PDF/DOCX/TXT). "
    "This demo runs fully offline using local Sentence-Transformers & FAISS. No paid APIs."
)

# ------------------- Load embeddings model ------------------- #
with st.spinner("Loading embeddings model..."):
    get_model()  # ensures model is loaded/downloaded before ranking

# ---------------- Sidebar ---------------- #
with st.sidebar:
    st.header("Input")
    jd_text = st.text_area("Paste Job Description (or upload file below)", height=220)
    jd_file = st.file_uploader("Upload JD (txt / pdf / docx)", type=["txt", "pdf", "docx"])
    resume_files = st.file_uploader(
        "Upload resumes (pdf / docx / txt) — multiple",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )
    top_k = st.slider("Top K results", min_value=1, max_value=20, value=5)

    st.markdown("---")
    st.header("Saved runs")
    init_db()
    runs = get_runs(limit=10)
    if runs:
        for r in runs:
            if st.button(f"Load run #{r['id']} — {r['timestamp']}", key=f"run_{r['id']}"):
                st.session_state["load_run_id"] = r["id"]

# ---------------- Load JD from file if provided ---------------- #
if jd_file is not None:
    jd_text = extract_text_from_file(jd_file)

# ---------------- Load saved run ---------------- #
if "load_run_id" in st.session_state:
    run_id = st.session_state["load_run_id"]
    st.header(f"Results for run #{run_id}")
    candidates = get_candidates_for_run(run_id)
    if not candidates:
        st.info("No candidates saved for this run.")
    else:
        df = pd.DataFrame(candidates)
        st.dataframe(df)
    st.stop()

# ---------------- Validate inputs ---------------- #
if not jd_text or len(jd_text.strip()) < 20:
    st.info("Please paste or upload a job description (at least 20 characters).")
    st.stop()

if not resume_files or len(resume_files) == 0:
    st.info("Upload at least one resume to rank.")
    st.stop()

# ---------------- Extract resume texts ---------------- #
st.info(f"Extracting text from {len(resume_files)} resumes...")
resumes = []
for f in resume_files:
    text = extract_text_from_file(f)
    resumes.append({"filename": f.name, "text": text})

# ---------------- Run ranking ---------------- #
with st.spinner("Computing embeddings and ranking..."):
    ranked = rank_resumes_by_jd(jd_text, resumes, top_k=top_k)

st.success("Ranking complete")

# ---------------- Save run to DB ---------------- #
if st.button("Save run to local DB"):
    run_id = create_run(jd_text)
    for r in ranked:
        save_candidate(
            run_id,
            r["filename"],
            r["sim_score"],
            r["keyword_score"],
            r["combined_score"],
            r["matched_keywords"],
            r["missing_keywords"],
        )
    st.success(f"Saved run #{run_id}. You can view it from the sidebar under 'Saved runs'.")

# ---------------- Display results ---------------- #
st.header("Ranked Candidates")
rows_for_csv = []

for i, r in enumerate(ranked, start=1):
    cols = st.columns([3, 1, 2, 2])
    cols[0].markdown(f"**{i}. {r['filename']}**")
    excerpt = (r["text"] or "").strip().replace("\n", " ")[:450]
    cols[0].write(excerpt + ("..." if len(excerpt) >= 450 else ""))
    cols[1].write(f"{r['sim_score']:.3f}")
    cols[2].write(f"{r['keyword_score']:.2f} ({len(r['matched_keywords'])} matched)")
    cols[3].write(f"{r['combined_score']:.3f}")

    if cols[0].button(f"Explain {r['filename']}", key=f"explain_{i}"):
        with st.spinner("Generating explanation..."):
            explanation = explain_candidate(jd_text, r["text"], top_n_keywords=6)
            st.info(explanation)

    rows_for_csv.append({
        "rank": i,
        "filename": r["filename"],
        "sim_score": r["sim_score"],
        "keyword_score": r["keyword_score"],
        "combined_score": r["combined_score"],
        "matched_keywords": ";".join(r["matched_keywords"]),
        "missing_keywords": ";".join(r["missing_keywords"])
    })

# ---------------- CSV Export ---------------- #
df = pd.DataFrame(rows_for_csv)
csv_data = df.to_csv(index=False)
st.download_button(
    label="Download Shortlist (CSV)",
    data=csv_data,
    file_name="shortlist.csv",
    mime="text/csv"
)
