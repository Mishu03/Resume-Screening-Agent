# app/matcher.py
from embedding_engine import compute_embeddings, normalize_embeddings
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def extract_top_keywords(jd_text: str, max_features: int = 80, top_n: int = 20):
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=max_features)
    try:
        tfidf = vectorizer.fit_transform([jd_text])
        features = vectorizer.get_feature_names_out()
        scores = tfidf.toarray().flatten()
        idx_sorted = list(scores.argsort()[::-1])
        keywords = [features[i] for i in idx_sorted if scores[i] > 0][:top_n]
        return keywords
    except Exception:
        return []

def match_keywords(text: str, keywords):
    text_low = (text or "").lower()
    return [kw for kw in keywords if kw.lower() in text_low]

def rank_resumes_by_jd(jd_text: str, resumes: list, top_k: int = 10):
    if not resumes:
        return []

    texts = [jd_text] + [r.get("text", "") for r in resumes]
    embs = compute_embeddings(texts)
    embs = normalize_embeddings(embs)

    jd_emb = embs[0:1]
    res_embs = embs[1:]

    sims = (res_embs @ jd_emb.T).squeeze()
    if isinstance(sims, np.float32) or (hasattr(sims, "ndim") and sims.ndim == 0):
        sims = np.array([float(sims)])

    sims = sims.tolist()
    keywords = extract_top_keywords(jd_text, max_features=120, top_n=20)

    results = []
    for i, r in enumerate(resumes):
        text = r.get("text", "") or ""
        matched = match_keywords(text, keywords)
        keyword_score = len(matched) / max(1, len(keywords))
        sim_score = float(sims[i])
        combined = 0.75 * sim_score + 0.25 * keyword_score

        missing = [k for k in keywords if k not in matched][:10]

        results.append({
            "filename": r.get("filename", f"resume_{i+1}"),
            "text": text,
            "sim_score": sim_score,
            "keyword_score": keyword_score,
            "combined_score": combined,
            "matched_keywords": matched,
            "missing_keywords": missing,
        })

    return sorted(results, key=lambda x: x["combined_score"], reverse=True)[:top_k]
