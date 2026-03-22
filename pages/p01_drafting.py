import streamlit as st
from core.tools import draft_document
from ui.components import page_header, run_button, copy_text_area, download_text, lang_selector
from ui.translations import t
from data.courts import COURTS, DOCUMENT_TYPES, STATES


def render():
    page_header(t("tool_drafting"), "दस्तावेज़ मसौदा", "दस्तावेज मसुदा")

    # ── Row 1: Document category → Document type ───────────────────────────────
    r1c1, r1c2, r1c3 = st.columns(3)

    with r1c1:
        doc_categories = [t("ph_select_category")] + list(DOCUMENT_TYPES.keys())
        sel_doc_cat = st.selectbox(t("doc_category"), options=doc_categories, key="draft_doc_cat")

    with r1c2:
        if sel_doc_cat and not sel_doc_cat.startswith("—"):
            doc_opts = [t("ph_select_type")] + DOCUMENT_TYPES[sel_doc_cat]
        else:
            doc_opts = [t("ph_select_first")]
        sel_doc = st.selectbox(t("doc_type"), options=doc_opts, key="draft_doc_type")
        doc_type = "" if sel_doc.startswith("—") else sel_doc

    with r1c3:
        language = lang_selector("draft_lang")

    # ── Row 2: Court category → Court name → State ────────────────────────────
    r2c1, r2c2, r2c3 = st.columns(3)

    with r2c1:
        court_categories = [t("ph_select_category")] + list(COURTS.keys())
        sel_court_cat = st.selectbox(t("court_category"), options=court_categories, key="draft_court_cat")

    with r2c2:
        if sel_court_cat and not sel_court_cat.startswith("—"):
            court_opts = [t("ph_select_court")] + COURTS[sel_court_cat]
        else:
            court_opts = [t("ph_select_first")]
        sel_court = st.selectbox(t("court"), options=court_opts, key="draft_court")
        court = "" if sel_court.startswith("—") else sel_court

    with r2c3:
        state_opts = [t("ph_select_state")] + STATES
        sel_state = st.selectbox(t("state"), options=state_opts, key="draft_state")
        state = "" if sel_state.startswith("—") else sel_state

    # ── Confirmation strip ────────────────────────────────────────────────────
    selected_parts = []
    if doc_type: selected_parts.append(f"📄 {doc_type}")
    if court:    selected_parts.append(f"🏛️ {court}")
    if state:    selected_parts.append(f"📍 {state}")
    if selected_parts:
        st.success("  ·  ".join(selected_parts))

    # ── Parties ───────────────────────────────────────────────────────────────
    party_details = st.text_input(
        t("parties"),
        placeholder=t("ph_parties"),
        key="draft_parties",
    )

    # ── Facts / Instructions ──────────────────────────────────────────────────
    facts = st.text_area(
        t("facts"),
        height=180,
        placeholder=t("ph_facts"),
        key="draft_facts",
    )

    court_full = f"{court}, {state}" if court and state else court or state or ""

    if run_button(t("btn_draft"), t("btn_draft"), "draft_run", disabled=not facts.strip()):
        with st.spinner(t("spinner_drafting")):
            try:
                result = draft_document(doc_type, facts, court_full, party_details, language)
                st.session_state["draft_result"] = result
                st.session_state["draft_config"] = {
                    "doc_type": doc_type, "court": court_full, "language": language
                }
            except Exception as e:
                st.error(f"Error: {e}")

    # ── Results ───────────────────────────────────────────────────────────────
    if "draft_result" in st.session_state:
        r = st.session_state["draft_result"]
        cfg = st.session_state.get("draft_config", {})
        st.markdown("---")

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"**{t('lbl_document')}** {r.get('title', '')}")
        with m2:
            st.markdown(f"**{t('lbl_court_out')}** {cfg.get('court', '—')}")
        with m3:
            sections = r.get("sections_included", [])
            st.markdown(
                f"**{t('lbl_sections')}** {', '.join(sections[:3])}"
                f"{'...' if len(sections) > 3 else ''}"
            )

        notes = r.get("notes", [])
        if notes:
            with st.expander(t("exp_placeholders")):
                for n in notes:
                    st.markdown(f"- {n}")

        st.markdown(f"**{t('lbl_edited_draft')}**")
        draft_text = r.get("document", "")
        edited = copy_text_area(draft_text, "draft_edit", height=500)

        # ── Download row ──────────────────────────────────────────────────────
        dl_col, reset_col, _ = st.columns([1, 1, 2])
        with dl_col:
            download_text(edited, "drafted-document.txt", t("btn_download_draft"))
        with reset_col:
            if st.button(t("btn_clear"), key="draft_clear"):
                st.session_state.pop("draft_result", None)
                st.session_state.pop("draft_config", None)
                st.rerun()

        # ── Formatted .docx download ──────────────────────────────────────────
        from ui.docx_download import render_docx_download
        render_docx_download(
            draft_text=edited,
            court=cfg.get("court", "").split(",")[0].strip(),
            doc_type=doc_type,
            party_details=party_details,
            state=state,
            language=cfg.get("language", "English"),
            key_prefix="draft",
        )
