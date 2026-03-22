import re


def detect_language(text: str) -> dict:
    """
    Detect language of a legal document.
    Returns dict with language label, script ratio, and confidence.

    Supports: English, Hindi, Marathi, Mixed
    """
    if not text or len(text.strip()) < 10:
        return {"label": "Unknown", "script": "unknown", "confidence": "low"}

    # Count Devanagari characters (covers both Hindi and Marathi)
    devanagari_chars = re.findall(r"[\u0900-\u097F]", text)
    latin_chars = re.findall(r"[a-zA-Z]", text)

    total = len(devanagari_chars) + len(latin_chars)
    if total == 0:
        return {"label": "Unknown", "script": "unknown", "confidence": "low"}

    dev_ratio = len(devanagari_chars) / total

    # Marathi-specific common words and legal terms
    marathi_patterns = [
        r"आहे", r"नाही", r"केले", r"होते", r"आणि", r"परंतु",
        r"याचिका", r"अर्जदार", r"विरुद्ध", r"न्यायालय",
        r"मुंबई", r"महाराष्ट्र", r"दाखल", r"आदेश",
        r"साठी", r"त्यांनी", r"यांनी", r"करण्यात",
    ]

    # Hindi-specific legal terms
    hindi_patterns = [
        r"याचिकाकर्ता", r"प्रतिवादी", r"न्यायाधीश",
        r"उच्च न्यायालय", r"सर्वोच्च न्यायालय",
        r"आवेदन", r"माननीय", r"अभियुक्त",
        r"दिनांक", r"बनाम", r"एवं", r"तथा",
    ]

    marathi_score = sum(1 for p in marathi_patterns if re.search(p, text))
    hindi_score = sum(1 for p in hindi_patterns if re.search(p, text))

    # Determine language
    if dev_ratio < 0.05:
        label = "English"
        script = "latin"
        confidence = "high" if dev_ratio < 0.01 else "medium"

    elif dev_ratio > 0.75:
        if marathi_score > hindi_score:
            label = "Marathi / मराठी"
            script = "devanagari"
        elif hindi_score > marathi_score:
            label = "Hindi / हिंदी"
            script = "devanagari"
        else:
            label = "Hindi / हिंदी"  # default to Hindi if unclear
            script = "devanagari"
        confidence = "high"

    else:
        # Mixed document
        if marathi_score > hindi_score:
            label = "Mixed (English + Marathi)"
        elif hindi_score > marathi_score:
            label = "Mixed (English + Hindi)"
        elif marathi_score > 0 and hindi_score > 0:
            label = "Mixed (Trilingual)"
        else:
            label = "Mixed (English + Devanagari)"
        script = "mixed"
        confidence = "medium"

    return {
        "label": label,
        "script": script,
        "confidence": confidence,
        "dev_ratio": round(dev_ratio, 2),
        "marathi_score": marathi_score,
        "hindi_score": hindi_score,
    }


def get_language_emoji(label: str) -> str:
    """Return a flag/symbol for the detected language."""
    if "Marathi" in label:
        return "🟠"  # Maharashtra saffron
    elif "Hindi" in label:
        return "🔵"
    elif "Mixed" in label:
        return "🟡"
    else:
        return "⚪"


def get_script_note(lang_info: dict) -> str:
    """Return a human-readable note about the document's language."""
    label = lang_info.get("label", "Unknown")
    confidence = lang_info.get("confidence", "low")

    note = f"Detected: **{label}**"
    if confidence == "medium":
        note += " *(mixed script document)*"
    return note
