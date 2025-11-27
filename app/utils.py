# app/utils.py
import re

def short_text(text: str, max_chars: int = 400) -> str:
    if not text:
        return ""
    s = text.replace("\n", " ").strip()
    if len(s) <= max_chars:
        return s
    return s[:max_chars].rstrip() + "..."
