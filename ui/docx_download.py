"""
ui/docx_download.py
Reusable download widget that generates a formatted .docx and
renders a download button with format info summary.
"""
import streamlit as st
from ui.translations import t


def render_docx_download(
    draft_text: str,
    court: str = "",
    doc_type: str = "",
    party_details: str = "",
    case_number: str = "",
    state: str = "",
    advocate_name: str = "",
    advocate_enrolment: str = "",
    language: str = "English",
    key_prefix: str = "draft",
):
    """
    Render a collapsible section showing the court format details
    and a one-click .docx download button.
    """
    from core.court_formatter import create_court_document, get_court_profile_summary

    profile_info = get_court_profile_summary(court)

    with st.expander("📥 Download as formatted court document (.docx)", expanded=True):
        # ── Format info strip ──────────────────────────────────────────────────
        st.markdown(
            "<p style='font-size:0.82rem;color:#7a6a52;margin-bottom:10px;'>"
            "The .docx file will be formatted as per the selected court's rules — "
            "correct font, margins, spacing, header, footer, and verification page.</p>",
            unsafe_allow_html=True,
        )

        cols = st.columns(3)
        with cols[0]:
            st.markdown(
                f"<div style='background:#f7f4ee;border-radius:8px;padding:10px 14px;"
                f"font-size:0.82rem;'>"
                f"<div style='font-size:0.7rem;color:#7a6a52;text-transform:uppercase;"
                f"letter-spacing:0.06em;margin-bottom:3px;'>Font &amp; Size</div>"
                f"<strong>{profile_info['font']}</strong></div>",
                unsafe_allow_html=True,
            )
        with cols[1]:
            st.markdown(
                f"<div style='background:#f7f4ee;border-radius:8px;padding:10px 14px;"
                f"font-size:0.82rem;'>"
                f"<div style='font-size:0.7rem;color:#7a6a52;text-transform:uppercase;"
                f"letter-spacing:0.06em;margin-bottom:3px;'>Line Spacing &amp; Margins</div>"
                f"<strong>{profile_info['line_spacing']}</strong> · {profile_info['margins']}</div>",
                unsafe_allow_html=True,
            )
        with cols[2]:
            st.markdown(
                f"<div style='background:#f7f4ee;border-radius:8px;padding:10px 14px;"
                f"font-size:0.82rem;'>"
                f"<div style='font-size:0.7rem;color:#7a6a52;text-transform:uppercase;"
                f"letter-spacing:0.06em;margin-bottom:3px;'>Verification Page</div>"
                f"<strong>{profile_info['verification']}</strong></div>",
                unsafe_allow_html=True,
            )

        st.markdown("")

        # ── Advocate details (optional, fills signature block) ─────────────────
        adv_col1, adv_col2, adv_col3 = st.columns(3)
        with adv_col1:
            adv_name = st.text_input(
                "Advocate name (for signature block)",
                value=advocate_name,
                placeholder="e.g. Adv. Priya Desai",
                key=f"{key_prefix}_adv_name",
            )
        with adv_col2:
            adv_enrol = st.text_input(
                "Enrolment number",
                value=advocate_enrolment,
                placeholder="e.g. MH/1234/2010",
                key=f"{key_prefix}_adv_enrol",
            )
        with adv_col3:
            case_no = st.text_input(
                "Case number",
                value=case_number,
                placeholder="e.g. 1234/2025",
                key=f"{key_prefix}_case_no",
            )

        # ── Generate and download ──────────────────────────────────────────────
        if st.button(
            "⬇️  Generate & download .docx",
            key=f"{key_prefix}_docx_btn",
            use_container_width=True,
        ):
            with st.spinner("Generating formatted court document..."):
                try:
                    docx_bytes = create_court_document(
                        draft_text=draft_text,
                        court=court,
                        doc_type=doc_type,
                        party_details=party_details,
                        case_number=case_no,
                        state=state,
                        advocate_name=adv_name or advocate_name,
                        advocate_enrolment=adv_enrol or advocate_enrolment,
                        language=language,
                    )
                    st.session_state[f"{key_prefix}_docx_bytes"] = docx_bytes
                    st.success("✅ Document ready — click below to download")
                except Exception as e:
                    st.error(f"Could not generate .docx: {e}")

        # Show download button once generated
        if f"{key_prefix}_docx_bytes" in st.session_state:
            filename = _safe_filename(doc_type, court)
            st.download_button(
                label=f"💾  Save  {filename}",
                data=st.session_state[f"{key_prefix}_docx_bytes"],
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key=f"{key_prefix}_docx_dl",
                use_container_width=True,
            )
            st.caption(
                "Open in Microsoft Word, LibreOffice, or Google Docs. "
                "Fill in the [___] placeholders highlighted in the document."
            )


def _safe_filename(doc_type: str, court: str) -> str:
    """Generate a clean filename from doc type and court."""
    import re
    parts = []
    if doc_type:
        clean = re.sub(r"[^\w\s-]", "", doc_type).strip().replace(" ", "_")
        parts.append(clean[:30])
    if court:
        court_short = court.split("(")[0].strip().split(",")[0].strip()
        court_clean = re.sub(r"[^\w\s-]", "", court_short).strip().replace(" ", "_")
        parts.append(court_clean[:20])
    if not parts:
        parts.append("Legal_Document")
    return "_".join(parts) + ".docx"
