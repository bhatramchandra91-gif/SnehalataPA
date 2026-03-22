"""ui/components.py — Reusable UI components for all pages."""
import streamlit as st

RISK_CSS = {"high": "issue-error", "medium": "issue-warning", "low": "issue-ok"}
STATUS_EMOJI = {"pass": "✅", "warn": "⚠️", "fail": "❌",
                "compliant": "✅", "non_compliant": "❌", "needs_review": "⚠️",
                "clean": "✅", "minor_issues": "⚠️", "significant_issues": "🔴", "deal_breaker": "❌"}
URGENCY_EMOJI = {"high": "🔴", "med": "🟡", "low": "🟢",
                 "immediate": "🔴", "within_30_days": "🟡", "within_90_days": "🟢"}


def page_header(title_en: str, title_hi: str, title_mr: str = ""):
    """Render standard page header with tricolour accent."""
    st.markdown(f"""
    <div style='border-left:4px solid #d4500a;padding-left:14px;margin-bottom:1.2rem;'>
        <h2 style='font-family:"Crimson Pro",serif;font-size:1.7rem;color:#0d2240;
                   margin:0 0 2px 0;line-height:1.2;'>{title_en}</h2>
        <p style='font-family:"Tiro Devanagari Hindi",serif;font-size:0.85rem;
                  color:#7a6a52;margin:0;'>{title_hi}{" · " + title_mr if title_mr else ""}</p>
    </div>
    """, unsafe_allow_html=True)


def status_badge(status: str, label: str = "") -> str:
    css_map = {
        "pass": "status-pass", "warn": "status-warn", "fail": "status-fail",
        "high": "status-fail", "medium": "status-warn", "low": "status-pass",
        "compliant": "status-pass", "non_compliant": "status-fail", "needs_review": "status-warn",
        "clean": "status-pass", "significant_issues": "status-fail", "deal_breaker": "status-fail",
    }
    css = css_map.get(status, "status-warn")
    display = label or status.replace("_", " ").title()
    return f'<span class="{css}">{display}</span>'


def issue_card(text: str, issue_type: str = "info", hi_text: str = "",
               sub_text: str = ""):
    """Render a colored issue/finding card."""
    css = {"ok": "issue-ok", "warning": "issue-warning", "error": "issue-error",
           "info": "issue-info"}.get(issue_type, "issue-info")
    hi_html = f"<span class='issue-hi'>{hi_text}</span>" if hi_text else ""
    sub_html = f"<span style='font-size:0.8rem;opacity:0.75;display:block;margin-top:3px;'>{sub_text}</span>" if sub_text else ""
    st.markdown(f"<div class='{css}'>{text}{hi_html}{sub_html}</div>", unsafe_allow_html=True)


def overall_banner(status: str, messages: dict):
    css_map = {"pass": "overall-pass", "warn": "overall-warn", "fail": "overall-fail",
               "low": "overall-pass", "medium": "overall-warn", "high": "overall-fail",
               "clean": "overall-pass", "minor_issues": "overall-warn",
               "significant_issues": "overall-fail", "deal_breaker": "overall-fail",
               "compliant": "overall-pass", "partial": "overall-warn", "non_compliant": "overall-fail"}
    css = css_map.get(status, "overall-warn")
    msg = messages.get(status, f"Status: {status}")
    st.markdown(f"<div class='{css}'>{STATUS_EMOJI.get(status,'')} {msg}</div>", unsafe_allow_html=True)
    st.markdown("")


def deadline_row(date: str, description: str, date_type: str = "", urgency: str = "low", hi: str = ""):
    hi_html = f"<span class='issue-hi'>{hi}</span>" if hi else ""
    st.markdown(f"""
    <div class='deadline-row'>
        <div><div class='deadline-date'>{date}</div>
             <div style='font-size:0.7rem;color:#7a6a52;'>{date_type}</div></div>
        <div style='flex:1'>{URGENCY_EMOJI.get(urgency,'⚪')} {description}{hi_html}</div>
    </div>""", unsafe_allow_html=True)


def doc_input_tabs(key_prefix: str, height: int = 200,
                   placeholder: str = "") -> str:
    """Return extracted document text from paste or upload tabs."""
    from core.pdf_reader import extract_text, get_word_count
    from core.language import detect_language, get_script_note
    from ui.translations import t

    if not placeholder:
        placeholder = t("ph_paste_doc")

    tab_paste, tab_upload = st.tabs([t("tab_paste"), t("tab_upload")])
    doc_text = ""

    with tab_paste:
        st.markdown(
            f"<p style='font-size:0.82rem;color:#7a6a52;margin-bottom:4px;'>"
            f"{t('info_paste_any_lang')}</p>",
            unsafe_allow_html=True,
        )
        pasted = st.text_area("text", label_visibility="collapsed",
                              height=height, placeholder=placeholder, key=f"{key_prefix}_paste")
        if pasted.strip():
            doc_text = pasted
            lang = detect_language(pasted)
            st.markdown(
                f"<div class='lang-detected-box'>🌐 {get_script_note(lang)} · {get_word_count(pasted):,} words</div>",
                unsafe_allow_html=True)

    with tab_upload:
        uploaded = st.file_uploader("file", type=["pdf", "docx", "txt"],
                                    label_visibility="collapsed", key=f"{key_prefix}_upload")
        if uploaded:
            with st.spinner(t("spinner_analysing")):
                try:
                    extracted, ftype = extract_text(uploaded)
                    doc_text = extracted
                    lang = detect_language(extracted)
                    st.success(f"✅ {ftype} — {get_word_count(extracted):,} words · {get_script_note(lang)}")
                    with st.expander(t("exp_preview")):
                        st.text(extracted[:1000] + ("..." if len(extracted) > 1000 else ""))
                except Exception as e:
                    st.error(f"Extraction failed: {e}")
    return doc_text


def lang_selector(key: str = "lang") -> str:
    from ui.translations import t
    return st.selectbox(t("output_language"), ["English", "Hindi", "Marathi", "English + Hindi"], key=key)


def run_button(label_en: str, label_hi: str, key: str, disabled: bool = False):
    return st.button(f"{label_en}  ·  {label_hi}", key=key,
                     disabled=disabled, use_container_width=True)


def download_text(text: str, filename: str, label: str = "⬇️ Download"):
    st.download_button(label, data=text.encode("utf-8"),
                       file_name=filename, mime="text/plain;charset=utf-8")


def copy_text_area(text: str, key: str, height: int = 200, label: str = ""):
    """Show editable text area (good for draft output)."""
    if label:
        st.markdown(f"**{label}**")
    return st.text_area("draft", value=text, height=height,
                        label_visibility="collapsed", key=key)
