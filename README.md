# Resume Screening Agent — 100% Free (Local Models)

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.20-brightgreen)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Overview
The **Resume Screening Agent** ranks candidate resumes against a Job Description (JD) using **local embeddings** and **keyword matching** — no paid APIs required.

Ideal for:
- Cost-free demos
- Privacy-conscious deployments
- Quick AI prototyping

---

## Features
- Upload **Job Description** (TXT / PDF / DOCX)
- Upload multiple **resumes** (TXT / PDF / DOCX)
- **Semantic ranking** using local Sentence-Transformers embeddings
- **Keyword extraction** from JD using TF-IDF
- **Rule-based explanations**: matched/missing keywords, experience, seniority
- **Export ranked shortlist** as CSV
- Simple **Streamlit UI**, fully local, no API keys

---

## Tech Stack
- **UI:** Streamlit
- **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Vector search:** FAISS (IndexFlatIP)
- **Keyword extraction:** scikit-learn TF-IDF
- **File parsing:** pdfminer, docx2txt

---

## Screenshots

**Upload Job Description & Resumes**  

![Upload JD and Resumes](https://via.placeholder.com/800x400.png?text=Upload+JD+and+Resumes)

**Ranked Candidates with Explanations**  

![Ranked Candidates](https://via.placeholder.com/800x400.png?text=Ranked+Candidates+and+Explanations)

*Replace these URLs with real screenshots or GIFs of your app.*

---

## Setup & Run

```bash
# Clone repository
git clone <your-repo-url>
cd resume-screening-agent

# Create virtual environment
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app/main.py
