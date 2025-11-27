# app/resume_parser.py
import tempfile
import os
from pdfminer.high_level import extract_text as pdf_extract_text
import docx2txt

def extract_text_from_file(uploaded_file) -> str:
    """
    Accepts Streamlit UploadedFile or a path-like string.
    Returns extracted text (best-effort).
    """
    filename = getattr(uploaded_file, "name", None)
    if filename:
        ext = filename.split(".")[-1].lower()
    else:
        ext = str(uploaded_file).split(".")[-1].lower()

    # If uploaded_file has .read(), treat as stream
    content_bytes = None
    try:
        content_bytes = uploaded_file.read()
    except Exception:
        content_bytes = None

    if ext == "pdf":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            if content_bytes is not None:
                tmp.write(content_bytes)
            else:
                with open(uploaded_file, "rb") as f:
                    tmp.write(f.read())
            tmp.flush()
            try:
                text = pdf_extract_text(tmp.name)
            except Exception:
                text = ""
        try:
            os.unlink(tmp.name)
        except Exception:
            pass
        return text or ""
    elif ext in ("doc", "docx"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            if content_bytes is not None:
                tmp.write(content_bytes)
            else:
                with open(uploaded_file, "rb") as f:
                    tmp.write(f.read())
            tmp.flush()
            try:
                text = docx2txt.process(tmp.name)
            except Exception:
                text = ""
        try:
            os.unlink(tmp.name)
        except Exception:
            pass
        return text or ""
    else:
        # text fallback
        if content_bytes is None:
            try:
                with open(uploaded_file, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                return ""
        try:
            return content_bytes.decode("utf-8", errors="replace")
        except Exception:
            return str(content_bytes)
