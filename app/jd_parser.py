# app/jd_parser.py
import re

def clean_jd_text(text: str) -> str:
    """
    Basic JD cleaning: remove excessive whitespace, bullets normalization,
    and simple line merging.
    """
    if not text:
        return ""
    # Normalize bullets to hyphens
    text = text.replace("•", "-").replace("–", "-")
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Trim
    text = text.strip()
    return text
