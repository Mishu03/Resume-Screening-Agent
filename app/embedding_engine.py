# app/embedding_engine.py
from sentence_transformers import SentenceTransformer
import numpy as np
import torch
import streamlit as st

_MODEL = None
_MODEL_NAME = "all-MiniLM-L6-v2"

def get_model():
    """
    Safely load the Sentence-Transformers model.
    If not downloaded, show a Streamlit spinner while downloading.
    """
    global _MODEL
    if _MODEL is None:
        device = "cpu"  # Force CPU

        try:
            _MODEL = SentenceTransformer(_MODEL_NAME, device=device)
        except OSError:
            # If model is missing/corrupted, download while showing UI
            with st.spinner(f"Downloading model {_MODEL_NAME}... This may take a minute."):
                _MODEL = SentenceTransformer(_MODEL_NAME, device=device)
    return _MODEL

def compute_embeddings(texts, show_progress=False):
    """
    Compute embeddings for a list of texts.
    Returns: np.ndarray (n, dim)
    """
    model = get_model()
    embs = model.encode(texts, show_progress_bar=show_progress, convert_to_numpy=True)
    return embs.astype("float32")

def normalize_embeddings(embs):
    """
    Normalize embeddings to unit length (L2 norm)
    """
    norms = np.linalg.norm(embs, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return embs / norms
