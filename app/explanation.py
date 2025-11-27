# app/explanation.py
import re
from matcher import extract_top_keywords

def explain_candidate(jd_text: str, resume_text: str, top_n_keywords: int = 6) -> str:
    jd_low = jd_text.lower()
    res_low = (resume_text or "").lower()

    keywords = extract_top_keywords(jd_text, max_features=80, top_n=top_n_keywords)
    matched = [kw for kw in keywords if kw.lower() in res_low]
    missing = [kw for kw in keywords if kw.lower() not in res_low]

    # years detection
    years = re.findall(r'(\d{1,2})\s*\+?\s*(?:years|yrs|year)', res_low)
    years_found = sorted([int(y) for y in years], reverse=True) if years else []
    years_str = ", ".join(str(y) + " yrs" for y in years_found[:3]) if years_found else "Not detected"

    # seniority clues
    seniority = None
    for kw in ["senior", "lead", "manager", "sr.", "principal", "intern", "junior", "jr."]:
        if kw in res_low:
            seniority = kw
            break

    matched_frac = len(matched) / max(1, len(keywords))
    if matched_frac >= 0.7:
        recommendation = "Strong fit"
    elif matched_frac >= 0.4:
        recommendation = "Good fit"
    else:
        recommendation = "Weak fit"

    lines = [
        f"Top JD keywords considered: {', '.join(keywords) if keywords else 'N/A'}",
        f"Matched keywords ({len(matched)}): {', '.join(matched) if matched else 'None'}",
        f"Missing keywords: {', '.join(missing) if missing else 'None'}",
        f"Years-of-experience mentions: {years_str}",
        f"Seniority clues: {seniority if seniority else 'Not detected'}",
        f"Recommendation: {recommendation}"
    ]
    return "\n".join(lines)
