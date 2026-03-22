import streamlit as st

st.set_page_config(
    page_title="Nyay Prep — Indian Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui.styles import CUSTOM_CSS
from ui.translations import t, render_lang_switcher, get_ui_lang

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.markdown("<div class='tricolour-strip'></div>", unsafe_allow_html=True)

# ── Tool definitions (icon, translation_key, route_key) ─────────────────────
TOOLS = [
    ("✍️",  "tool_drafting",       "drafting"),
    ("🔍",  "tool_research",        "research"),
    ("📄",  "tool_contract",        "contract"),
    ("✉️", "tool_client_comm",     "client_comm"),
    ("🔎",  "tool_due_diligence",   "due_diligence"),
    ("🗂️","tool_discovery",        "discovery"),
    ("✅",  "tool_compliance",      "compliance"),
    ("🧾",  "tool_billing",         "billing"),
    ("⚖️", "tool_court_filing",    "court_filing"),
    ("📝",  "tool_meeting_notes",   "meeting_notes"),
    ("🔬",  "tool_ip_patent",       "ip_patent"),
    ("🧠",  "tool_knowledge",       "knowledge"),
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style='text-align:center;padding:1rem 0 0.5rem;'>
        <div style='width:56px;height:56px;background:#d4500a;border-radius:50%;
            display:inline-flex;align-items:center;justify-content:center;
            font-family:"Tiro Devanagari Hindi",serif;font-size:24px;color:white;margin-bottom:6px;'>
            न्या
        </div>
        <div style='font-family:"Crimson Pro",serif;font-size:1.35rem;font-weight:600;color:white;'>
            Nyay Prep
        </div>
        <div style='font-family:"Tiro Devanagari Hindi",serif;font-size:0.78rem;
            color:rgba(255,255,255,0.45);margin-top:2px;'>
            भारतीय विधिक सहायक
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Language switcher ────────────────────────────────────────────────────
    render_lang_switcher()

    # ── Tool navigation ──────────────────────────────────────────────────────
    st.markdown(
        f"<div class='sidebar-section-title'>{t('tools_heading')}</div>",
        unsafe_allow_html=True,
    )

    if "active_tool" not in st.session_state:
        st.session_state["active_tool"] = "drafting"

    for icon, name_key, route_key in TOOLS:
        label = f"{icon}  {t(name_key)}"
        if st.button(label, key=f"nav_{route_key}", use_container_width=True):
            st.session_state["active_tool"] = route_key
            for k in list(st.session_state.keys()):
                if k.endswith("_result"):
                    del st.session_state[k]
            st.rerun()

    # ── Info ─────────────────────────────────────────────────────────────────
    st.markdown(
        f"<div class='sidebar-section-title' style='margin-top:1rem;'>{t('info_heading')}</div>",
        unsafe_allow_html=True,
    )
    st.markdown("""
    <div style='font-size:0.71rem;color:rgba(255,255,255,0.38);line-height:1.9;'>
        Powered by Claude (Anthropic)<br>
        CPC · CrPC · IPC · Evidence Act<br>
        Companies Act · Arbitration Act<br>
        DPDP Act · Consumer Protection<br>
        English · हिंदी · मराठी
    </div>
    """, unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
h_col, l_col = st.columns([2, 1])
with h_col:
    lang = get_ui_lang()
    subtitle_map = {
        "en": "Indian Legal Assistant · भारतीय विधिक सहायक · भारतीय कायदेशीर सहाय्यक",
        "hi": "भारतीय विधिक सहायक · Indian Legal Assistant · भारतीय कायदेशीर सहाय्यक",
        "mr": "भारतीय कायदेशीर सहाय्यक · भारतीय विधिक सहायक · Indian Legal Assistant",
    }
    st.markdown(f"""
    <h1 class='nyay-title'>Nyay Prep</h1>
    <p class='nyay-title-hi'>{subtitle_map.get(lang, subtitle_map['en'])}</p>
    """, unsafe_allow_html=True)

with l_col:
    active_lang = get_ui_lang()
    badges = {
        "en": "<span class='lang-badge lang-en' style='border:2px solid #d4500a;'>EN ✓</span> <span class='lang-badge lang-hi'>हिंदी</span> <span class='lang-badge lang-mr'>मराठी</span>",
        "hi": "<span class='lang-badge lang-en'>EN</span> <span class='lang-badge lang-hi' style='border:2px solid #138808;'>हिंदी ✓</span> <span class='lang-badge lang-mr'>मराठी</span>",
        "mr": "<span class='lang-badge lang-en'>EN</span> <span class='lang-badge lang-hi'>हिंदी</span> <span class='lang-badge lang-mr' style='border:2px solid #138808;'>मराठी ✓</span>",
    }
    st.markdown(
        f"<div style='padding-top:0.9rem;text-align:right;'>{badges.get(active_lang, badges['en'])}</div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Route to tool ─────────────────────────────────────────────────────────────
tool = st.session_state.get("active_tool", "drafting")

if tool == "drafting":
    from pages.p01_drafting import render
    render()
elif tool == "research":
    from pages.p02_research import render
    render()
elif tool == "contract":
    from pages.p03_to_p12 import render_contract
    render_contract()
elif tool == "client_comm":
    from pages.p03_to_p12 import render_client_comm
    render_client_comm()
elif tool == "due_diligence":
    from pages.p03_to_p12 import render_due_diligence
    render_due_diligence()
elif tool == "discovery":
    from pages.p03_to_p12 import render_discovery
    render_discovery()
elif tool == "compliance":
    from pages.p03_to_p12 import render_compliance
    render_compliance()
elif tool == "billing":
    from pages.p03_to_p12 import render_billing
    render_billing()
elif tool == "court_filing":
    from pages.p03_to_p12 import render_court_filing
    render_court_filing()
elif tool == "meeting_notes":
    from pages.p03_to_p12 import render_meeting_notes
    render_meeting_notes()
elif tool == "ip_patent":
    from pages.p03_to_p12 import render_ip_patent
    render_ip_patent()
elif tool == "knowledge":
    from pages.p03_to_p12 import render_knowledge
    render_knowledge()
