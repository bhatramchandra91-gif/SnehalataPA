import streamlit as st

STATUS_EMOJI = {"pass":"✅","warn":"⚠️","fail":"❌"}
STATUS_LABEL = {"pass":"Pass","warn":"Review needed","fail":"Issues found"}
URGENCY_EMOJI = {"high":"🔴","med":"🟡","low":"🟢"}
PRIORITY_LABEL = {"high":"Required","med":"Important","low":"Optional"}
ISSUE_CLASS = {"ok":"issue-ok","warning":"issue-warning","error":"issue-error","info":"issue-info"}

def render_all_results(result: dict):
    overall = result.get("overall","warn")
    lang = result.get("detectedLanguage","Unknown")
    msgs = {"pass":"✅ Document looks ready to file.",
            "warn":"⚠️ Some items need review before filing.",
            "fail":"❌ Issues found that must be resolved."}
    css = {"pass":"overall-pass","warn":"overall-warn","fail":"overall-fail"}.get(overall,"overall-warn")
    st.markdown(f"<div class='{css}'>{msgs.get(overall,'')} &nbsp;|&nbsp; Language: <strong>{lang}</strong></div>",
                unsafe_allow_html=True)
    st.markdown("")

    col1, col2 = st.columns(2)
    with col1: _render_issues_expander("format", result.get("format",{}), "📄 Format & citations", "प्रारूप जाँच")
    with col2: _render_issues_expander("exhibits", result.get("exhibits",{}), "🗂️ Exhibits & annexures", "प्रदर्श जाँच")
    _render_checklist(result.get("checklist",{}))
    _render_deadlines(result.get("deadlines",{}))

def _render_issues_expander(name, data, label_en, label_hi):
    status = data.get("status","warn")
    with st.expander(f"{STATUS_EMOJI.get(status,'')} **{label_en}** — {data.get('summary','')}", expanded=(status!="pass")):
        st.markdown(f"<span class='devanagari' style='font-size:0.75rem;color:#7a6a52;'>{label_hi}</span>", unsafe_allow_html=True)
        for item in data.get("issues",[]):
            itype = item.get("type","info")
            css = ISSUE_CLASS.get(itype,"issue-info")
            hi = f"<span class='issue-hi'>{item['hi']}</span>" if item.get("hi") else ""
            st.markdown(f"<div class='{css}'>{item.get('text','')}{hi}</div>", unsafe_allow_html=True)

def _render_checklist(data):
    status = data.get("status","warn")
    with st.expander(f"{STATUS_EMOJI.get(status,'')} **Filing checklist** — {data.get('summary','')}", expanded=True):
        items = data.get("items",[])
        for grp_label, priority in [("🔴 Required","high"),("🟡 Important","med"),("🟢 Optional","low")]:
            grp = [i for i in items if i.get("priority")==priority]
            if not grp: continue
            st.markdown(f"**{grp_label}**")
            for idx, item in enumerate(grp):
                c1,c2 = st.columns([0.85,0.15])
                with c1:
                    st.checkbox(item.get("text",""), key=f"cf_cb_{priority}_{idx}")
                    if item.get("hi"):
                        st.markdown(f"<span class='issue-hi'>{item['hi']}</span>", unsafe_allow_html=True)
                with c2:
                    css = {"high":"status-fail","med":"status-warn","low":"status-pass"}.get(priority,"status-warn")
                    st.markdown(f"<span class='{css}'>{PRIORITY_LABEL.get(priority,'')}</span>", unsafe_allow_html=True)

def _render_deadlines(data):
    status = data.get("status","warn")
    with st.expander(f"{STATUS_EMOJI.get(status,'')} **Dates & deadlines** — {data.get('summary','')}", expanded=(status!="pass")):
        items = data.get("items",[])
        if not items:
            st.info("No specific dates found.")
            return
        for item in items:
            urgency = item.get("urgency","low")
            hi_html = f"<span class='issue-hi'>{item['hi']}</span>" if item.get("hi") else ""
            st.markdown(f"""<div class='deadline-row'>
                <div><div class='deadline-date'>{item.get('date','—')}</div>
                     <div style='font-size:0.7rem;color:#7a6a52;'>{item.get('dateType','')}</div></div>
                <div style='flex:1'>{URGENCY_EMOJI.get(urgency,'⚪')} {item.get('description','')}{hi_html}</div>
            </div>""", unsafe_allow_html=True)
