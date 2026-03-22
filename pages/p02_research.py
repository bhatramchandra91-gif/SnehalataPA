import streamlit as st
from core.tools import research_legal_question
from ui.components import page_header
from ui.translations import t, run_button, issue_card, download_text, lang_selector, doc_input_tabs

AREAS = [
    "Auto-detect", "Constitutional Law", "Civil Procedure (CPC)",
    "Criminal Law (IPC/CrPC)", "Contract Law", "Property Law",
    "Family Law", "Corporate Law", "Tax Law", "Labour Law",
    "IP Law", "Environmental Law", "Consumer Law", "Banking Law",
    "Arbitration Law", "Service Law",
]

def render():
    page_header(t("tool_research"), "विधिक अनुसंधान", "कायदेशीर संशोधन")

    col1, col2 = st.columns([2, 1])
    with col1:
        area = st.selectbox(t("area_of_law"), AREAS, key="res_area")
    with col2:
        language = lang_selector("res_lang")

    question = st.text_area(
        t("question"),
        height=100,
        placeholder=(
            "Ask any Indian law question...\n"
            "e.g. Can a tenant be evicted without notice under Maharashtra Rent Control Act? "
            "What is the limitation period for filing a cheque bounce case under Section 138 NI Act?"
        ),
        key="res_question",
    )

    st.markdown("<p style='font-size:0.82rem;color:#7a6a52;margin:4px 0;'>"
                "Optional: paste a judgment or document to analyze</p>", unsafe_allow_html=True)
    doc_text = doc_input_tabs("res", height=150,
                               placeholder="Paste judgment / statute text here (optional)...")

    can_run = bool(question.strip())
    if run_button(t("btn_research"), t("btn_research"), "res_run", disabled=not can_run):
        with st.spinner(t("spinner_analysing")):
            try:
                result = research_legal_question(question, area if area != "Auto-detect" else "",
                                                  doc_text, language)
                st.session_state["res_result"] = result
            except Exception as e:
                st.error(f"Error: {e}")

    if "res_result" in st.session_state:
        r = st.session_state["res_result"]
        st.markdown("---")

        # Direct answer
        confidence = r.get("confidence", "medium")
        conf_css = {"high": "status-pass", "medium": "status-warn", "low": "status-fail"}.get(confidence, "status-warn")
        st.markdown(
            f"<div class='result-card'>"
            f"<div class='result-card-title'>{r.get('question_answered','')}</div>"
            f"<div style='margin-top:8px;font-size:1rem;'>{r.get('direct_answer','')}</div>"
            f"<div style='margin-top:8px;'><span class='{conf_css}'>Confidence: {confidence}</span></div>"
            f"</div>", unsafe_allow_html=True)

        # Hindi summary (always shown)
        if r.get("hi_summary"):
            st.markdown(
                f"<div class='lang-detected-box'><span style='font-family:\"Tiro Devanagari Hindi\",serif;'>"
                f"🇮🇳 {r['hi_summary']}</span></div>", unsafe_allow_html=True)

        # Detailed analysis
        with st.expander("📖 Detailed analysis", expanded=True):
            st.markdown(r.get("detailed_analysis", ""))

        # Statutes + Cases in columns
        col1, col2 = st.columns(2)
        with col1:
            statutes = r.get("relevant_statutes", [])
            with st.expander(f"📚 Relevant statutes ({len(statutes)})"):
                for s in statutes:
                    issue_card(f"**{s.get('act','')} — {s.get('section','')}**", "info",
                               sub_text=s.get("relevance",""))

        with col2:
            cases = r.get("key_cases", [])
            with st.expander(f"⚖️ Key cases ({len(cases)})"):
                for c in cases:
                    issue_card(f"**{c.get('case','')}** ({c.get('year','')})", "ok",
                               sub_text=f"{c.get('holding','')} — {c.get('relevance','')}")

        # Practical advice
        practical = r.get("practical_advice", [])
        if practical:
            with st.expander("🛠️ Practical advice"):
                for p in practical:
                    st.markdown(f"- {p}")

        if r.get("limitations"):
            st.info(f"⚠️ **Limitations:** {r['limitations']}")

        # Download
        summary = (f"LEGAL RESEARCH SUMMARY\n{'='*50}\n"
                   f"Question: {r.get('question_answered','')}\n\n"
                   f"Answer: {r.get('direct_answer','')}\n\n"
                   f"Analysis: {r.get('detailed_analysis','')}")
        download_text(summary, "legal-research.txt")
