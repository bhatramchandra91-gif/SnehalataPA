"""
pages/p03_to_p12.py
All remaining pages: Contract Review, Client Comms, Due Diligence,
Discovery, Compliance, Billing, Court Filing, Meeting Notes, IP Patent, Knowledge Mgmt
"""
import streamlit as st
from ui.components import (page_header, run_button, issue_card, overall_banner,
                            deadline_row, doc_input_tabs, lang_selector,
                            copy_text_area, download_text, status_badge, RISK_CSS)
from ui.translations import t
from core.tools import (review_contract, draft_client_communication, run_due_diligence,
                         support_discovery, check_compliance, generate_billing,
                         prepare_court_filing, process_meeting_notes,
                         support_ip_patent, knowledge_query)
from core.pdf_reader import truncate_for_api
from core.language import detect_language


# ══════════════════════════════════════════════════════════════════════════════
# P03 — CONTRACT REVIEW
# ══════════════════════════════════════════════════════════════════════════════
def render_contract():
    page_header("Contract Review", "अनुबंध समीक्षा", "करार पुनरावलोकन")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ct = st.selectbox(t("contract_type"), ["Auto-detect","Service Agreement","NDA",
            "Employment Contract","Lease Agreement","Sale Agreement","JV Agreement",
            "Loan Agreement","Franchise","Consultancy","Software License","MOU"], key="cr_type")
    with col2:
        role = st.selectbox(t("client_role"), ["Not specified","Service Provider","Service Recipient",
            "Employer","Employee","Landlord","Tenant","Buyer","Seller","Lender","Borrower"], key="cr_role")
    with col3:
        law = st.selectbox(t("governing_law"), ["Indian Law","Maharashtra","Delhi",
            "Karnataka","Tamil Nadu","Gujarat"], key="cr_law")
    with col4:
        lang = lang_selector("cr_lang")

    doc_text = doc_input_tabs("cr", placeholder="Paste contract text here...")

    if run_button(t("btn_review_contract"), t("btn_review_contract"), "cr_run", disabled=not doc_text.strip()):
        with st.spinner(t("spinner_analysing")):
            try:
                st.session_state["cr_result"] = review_contract(
                    doc_text, "" if ct=="Auto-detect" else ct,
                    "" if role=="Not specified" else role, law, lang)
            except Exception as e:
                st.error(f"Error: {e}")

    if "cr_result" in st.session_state:
        r = st.session_state["cr_result"]
        st.markdown("---")
        risk = r.get("overall_risk","medium")
        msgs = {"low":"🟢 Low risk — contract appears balanced.",
                "medium":"🟡 Medium risk — several clauses need attention.",
                "high":"🔴 High risk — significant issues. Do not sign without revisions."}
        overall_banner(risk, msgs)

        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Type", r.get("contract_type_detected","—"))
        m2.metric("Law", r.get("governing_law_detected","—"))
        m3.metric("Duration", r.get("duration","—"))
        m4.metric("Parties", str(len(r.get("parties",[]))))

        with st.expander(t("exp_summary"), expanded=True):
            st.write(r.get("contract_summary",""))
            for p in r.get("parties",[]): st.markdown(f"- {p}")

        risks = r.get("risk_clauses",[])
        with st.expander(f"⚠️ Risk clauses ({len(risks)})",
                         expanded=any(c.get("risk_level")=="high" for c in risks)):
            for c in sorted(risks, key=lambda x:{"high":0,"medium":1,"low":2}.get(x.get("risk_level","low"),1)):
                issue_card(f"**{c.get('clause','')}** — {c.get('issue','')}",
                           {"high":"error","medium":"warning","low":"ok"}.get(c.get("risk_level","medium"),"warning"),
                           c.get("hi",""), f"💡 {c.get('recommendation','')}")

        missing = r.get("missing_clauses",[])
        with st.expander(f"❌ Missing clauses ({len(missing)})"):
            for m in missing:
                issue_card(f"**{m.get('clause','')}** — {m.get('reason','')}",
                           {"high":"error","medium":"warning","low":"info"}.get(m.get("importance","medium"),"warning"))

        with st.expander("📌 Obligations"):
            obs = r.get("obligations",{})
            parties = r.get("parties",["Party 1","Party 2"])
            c1,c2 = st.columns(2)
            with c1:
                st.markdown(f"**{parties[0] if parties else 'Party 1'}**")
                for o in obs.get("party1",[]): st.markdown(f"- {o.get('text','')}{ ' *('+o['deadline']+')*' if o.get('deadline') else ''}")
            with c2:
                st.markdown(f"**{parties[1] if len(parties)>1 else 'Party 2'}**")
                for o in obs.get("party2",[]): st.markdown(f"- {o.get('text','')}{ ' *('+o['deadline']+')*' if o.get('deadline') else ''}")

        redlines = r.get("redline_suggestions",[])
        with st.expander(f"✏️ Redline suggestions ({len(redlines)})"):
            for rd in redlines:
                st.markdown(f"**{rd.get('reason','')}**")
                rc1,rc2 = st.columns(2)
                with rc1:
                    st.markdown("*Original:*")
                    issue_card(rd.get("original",""), "error")
                with rc2:
                    st.markdown("*Suggested:*")
                    issue_card(rd.get("suggested",""), "ok")
                st.markdown("")

        if r.get("dpdp_compliance"):
            with st.expander("🔒 DPDP Act 2023 compliance"):
                st.write(r["dpdp_compliance"])


# ══════════════════════════════════════════════════════════════════════════════
# P04 — CLIENT COMMUNICATION
# ══════════════════════════════════════════════════════════════════════════════
def render_client_comm():
    page_header("Client Communication", "मुवक्किल संचार", "अशील संपर्क")

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        comm_type = st.selectbox(t("comm_type"), ["Email","WhatsApp message","Letter",
            "SMS","Court notice letter"], key="cc_type")
    with col2:
        purpose = st.selectbox(t("purpose"), ["Case update","Hearing outcome",
            "Action required","Document request","Fee update",
            "Adverse order","Favorable order","Settlement","General update"], key="cc_purpose")
    with col3:
        tone = st.selectbox(t("tone"), ["Professional","Warm & empathetic",
            "Formal","Simple (non-legal client)"], key="cc_tone")
    with col4:
        lang = lang_selector("cc_lang")

    nc1,nc2,nc3 = st.columns(3)
    with nc1: client_name = st.text_input(t("client_name"), key="cc_client")
    with nc2: advocate_name = st.text_input(t("advocate_name"), key="cc_adv")
    with nc3: case_ref = st.text_input(t("case_ref"), key="cc_ref", placeholder="WP 1234/2025")

    update = st.text_area(t("case_notes"),height=160,
        placeholder="Describe what happened and what client needs to know...\n\n"
                   "Example: Hearing held today. Court granted ad-interim stay. "
                   "Next date 15 May 2025. Client must provide original documents by 10 May.",
        key="cc_notes")

    if run_button(t("btn_draft_comm"), t("btn_draft_comm"),"cc_run",disabled=not update.strip()):
        with st.spinner(t("spinner_analysing")):
            try:
                st.session_state["cc_result"] = draft_client_communication(
                    update, comm_type, client_name, advocate_name, case_ref, tone, lang)
            except Exception as e:
                st.error(f"Error: {e}")

    if "cc_result" in st.session_state:
        r = st.session_state["cc_result"]
        st.markdown("---")
        if r.get("plain_summary"):
            st.markdown(f"<div class='overall-pass'>📋 {r['plain_summary']}</div>", unsafe_allow_html=True)
            st.markdown("")

        actions = r.get("action_items",[])
        if actions:
            with st.expander("📌 Action items for client", expanded=True):
                for a in actions: st.markdown(f"- {a}")

        tab1, tab2 = st.tabs(["📧 Primary draft", "🌐 Hindi/Marathi version"])
        with tab1:
            if r.get("subject"): st.markdown(f"**Subject:** {r['subject']}")
            edited = copy_text_area(r.get("body",""), "cc_edit", 280)
            full = f"Subject: {r.get('subject','')}\n\n{edited}"
            download_text(full, "client-communication.txt")
        with tab2:
            if r.get("body_hi"):
                if r.get("subject_hi"): st.markdown(f"**Subject:** {r['subject_hi']}")
                edited_hi = copy_text_area(r["body_hi"], "cc_edit_hi", 280)
                download_text(f"Subject: {r.get('subject_hi','')}\n\n{edited_hi}", "client-comm-hi.txt")
            else:
                st.info("Select 'Hindi', 'Marathi', or 'English + Hindi' as output language.")

        if st.button("🔄 Regenerate", key="cc_regen"):
            st.session_state.pop("cc_result", None)
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# P05 — DUE DILIGENCE
# ══════════════════════════════════════════════════════════════════════════════
def render_due_diligence():
    page_header("Due Diligence", "उचित परिश्रम", "योग्य परिश्रम")

    col1,col2 = st.columns(2)
    with col1:
        dd_type = st.selectbox(t("dd_type"), ["Corporate","Legal","Financial","Property",
            "Employment","IP","Merger & Acquisition","Startup Investment"], key="dd_type")
    with col2:
        transaction = st.text_input(t("transaction"), key="dd_txn",
            placeholder="e.g. Acquisition of XYZ Pvt Ltd for ₹5 crore")

    lang = lang_selector("dd_lang")
    doc_text = doc_input_tabs("dd", placeholder="Paste documents for DD review...")

    if run_button(t("btn_due_diligence"), t("btn_due_diligence"),"dd_run",disabled=not doc_text.strip()):
        with st.spinner(t("spinner_analysing")):
            try:
                st.session_state["dd_result"] = run_due_diligence(doc_text, dd_type, transaction, lang)
            except Exception as e:
                st.error(f"Error: {e}")

    if "dd_result" in st.session_state:
        r = st.session_state["dd_result"]
        st.markdown("---")
        assessment = r.get("overall_assessment","minor_issues")
        msgs = {"clean":"✅ Clean — no major issues found.",
                "minor_issues":"🟡 Minor issues — review recommended before proceeding.",
                "significant_issues":"🔴 Significant issues — must be addressed.",
                "deal_breaker":"❌ Deal breaker issues found — do not proceed without resolution."}
        overall_banner(assessment, msgs)

        if r.get("transaction_summary"):
            st.markdown(f"**Transaction:** {r['transaction_summary']}")

        reds = r.get("red_flags",[])
        greens = r.get("green_flags",[])
        rf_col, gf_col = st.columns(2)
        with rf_col:
            with st.expander(f"🚩 Red flags ({len(reds)})", expanded=bool(reds)):
                for f in sorted(reds, key=lambda x:{"high":0,"medium":1,"low":2}.get(x.get("severity","medium"),1)):
                    issue_card(f"**{f.get('issue','')}**",
                               {"high":"error","medium":"warning","low":"info"}.get(f.get("severity","medium"),"warning"),
                               f.get("hi",""), f"💡 {f.get('recommendation','')}")
        with gf_col:
            with st.expander(f"✅ Green flags ({len(greens)})", expanded=True):
                for g in greens:
                    issue_card(g.get("item",""), "ok")

        docs = r.get("document_checklist",[])
        with st.expander(f"📁 Document checklist ({len(docs)})"):
            for d in docs:
                s = d.get("status","unclear")
                emoji = {"found":"✅","missing":"❌","unclear":"⚠️"}.get(s,"⚠️")
                st.markdown(f"{emoji} **{d.get('document','')}** "
                            f"<span class='status-{'pass' if s=='found' else 'fail' if s=='missing' else 'warn'}'>"
                            f"{s}</span>", unsafe_allow_html=True)

        compl = r.get("legal_compliance",[])
        with st.expander(f"⚖️ Legal compliance ({len(compl)})"):
            for c in compl:
                s = c.get("status","needs_review")
                issue_card(f"**{c.get('area','')}** — {c.get('notes','')}",
                           {"compliant":"ok","non_compliant":"error","needs_review":"warning"}.get(s,"warning"))

        recs = r.get("recommendations",[])
        if recs:
            with st.expander("📋 Recommendations"):
                for i,rec in enumerate(recs,1): st.markdown(f"{i}. {rec}")

        if r.get("summary_report"):
            with st.expander("📊 Executive summary"):
                st.write(r["summary_report"])
                download_text(r["summary_report"], "dd-report.txt", t("btn_download_report"))


# ══════════════════════════════════════════════════════════════════════════════
# P06 — DISCOVERY SUPPORT
# ══════════════════════════════════════════════════════════════════════════════
def render_discovery():
    page_header("Discovery Support", "खोज सहायता", "शोध सहाय्य")

    col1,col2,col3 = st.columns(3)
    with col1:
        case_type = st.selectbox(t("case_type"), ["Civil","Criminal","Arbitration",
            "Consumer","Labour","Family","Commercial"], key="ds_casetype")
    with col2:
        task = st.selectbox(t("task"), ["Full analysis","Timeline construction",
            "Evidence review","Witness prep questions",
            "Interrogatory drafting","Key facts extraction"], key="ds_task")
    with col3:
        lang = lang_selector("ds_lang")

    case_summary = st.text_input(t("case_summary"), key="ds_summary",
        placeholder="e.g. Contract dispute over non-payment of ₹20L for IT services")

    doc_text = doc_input_tabs("ds", height=180,
        placeholder="Paste case documents, pleadings, evidence here...")

    if run_button(t("btn_discovery"), t("btn_discovery"),"ds_run",disabled=not doc_text.strip()):
        with st.spinner(t("spinner_analysing")):
            try:
                st.session_state["ds_result"] = support_discovery(doc_text, case_type, case_summary, task, lang)
            except Exception as e:
                st.error(f"Error: {e}")

    if "ds_result" in st.session_state:
        r = st.session_state["ds_result"]
        st.markdown("---")
        if r.get("case_summary_detected"):
            st.info(f"📋 {r['case_summary_detected']}")

        str_col, weak_col = st.columns(2)
        with str_col:
            strengths = r.get("strengths_in_case",[])
            with st.expander(f"💪 Strengths ({len(strengths)})", expanded=True):
                for s in strengths: issue_card(s, "ok")
        with weak_col:
            weaknesses = r.get("weaknesses_in_case",[])
            with st.expander(f"⚠️ Weaknesses ({len(weaknesses)})", expanded=True):
                for w in weaknesses:
                    issue_card(w.get("weakness",""), "warning", sub_text=f"Mitigation: {w.get('mitigation','')}")

        facts = r.get("key_facts",[])
        with st.expander(f"📌 Key facts ({len(facts)})", expanded=True):
            for f in sorted(facts, key=lambda x:{"high":0,"medium":1,"low":2}.get(x.get("significance","low"),1)):
                sig = f.get("significance","low")
                issue_card(f.get("fact",""),
                           {"high":"error","medium":"warning","low":"info"}.get(sig,"info"),
                           sub_text=f"Source: {f.get('source','')} | Significance: {sig}")

        timeline = r.get("timeline",[])
        with st.expander(f"📅 Timeline ({len(timeline)})"):
            for t in timeline:
                deadline_row(t.get("date","—"), t.get("event",""), "Event",
                             "med" if t.get("significance") else "low")

        evidence = r.get("evidence_found",[])
        with st.expander(f"🗂️ Evidence ({len(evidence)})"):
            for e in evidence:
                strength = e.get("strength","moderate")
                issue_card(f"**{e.get('item','')}** [{e.get('type','')}]",
                           {"strong":"ok","moderate":"warning","weak":"error"}.get(strength,"warning"),
                           sub_text=e.get("admissibility_note",""))

        qs = r.get("interrogatory_questions",[])
        if qs:
            with st.expander(f"❓ Interrogatory questions ({len(qs)})"):
                qs_text = "\n".join(f"{i+1}. {q}" for i,q in enumerate(qs))
                st.text_area("Questions (copy these)", qs_text, height=200, key="ds_qs", label_visibility="collapsed")

        doc_reqs = r.get("document_requests",[])
        if doc_reqs:
            with st.expander(f"📂 Document requests ({len(doc_reqs)})"):
                for d in doc_reqs: st.markdown(f"- {d}")


# ══════════════════════════════════════════════════════════════════════════════
# P07 — COMPLIANCE CHECKS
# ══════════════════════════════════════════════════════════════════════════════
def render_compliance():
    page_header("Compliance Checks", "अनुपालन जाँच", "अनुपालन तपासणी")

    col1,col2,col3 = st.columns(3)
    with col1:
        industry = st.selectbox(t("industry"), ["General","Technology/IT","Manufacturing",
            "Banking & Finance","Healthcare","Real Estate","Retail/E-commerce",
            "Food & Beverage","Logistics","Media","Education"], key="comp_ind")
    with col2:
        company_type = st.selectbox(t("entity_type"), ["Private Limited","Public Limited",
            "LLP","Partnership","Proprietorship","NGO/Trust","Startup"], key="comp_co")
    with col3:
        lang = lang_selector("comp_lang")

    specific_laws = st.text_input(t("specific_laws"),
        placeholder="e.g. FEMA, POSH Act, GST", key="comp_laws")

    doc_text = doc_input_tabs("comp", placeholder="Paste company documents, agreements, or describe operations...")

    if run_button(t("btn_compliance"), t("btn_compliance"),"comp_run",disabled=not doc_text.strip()):
        with st.spinner(t("spinner_analysing")):
            try:
                st.session_state["comp_result"] = check_compliance(doc_text, industry, company_type, specific_laws, lang)
            except Exception as e:
                st.error(f"Error: {e}")

    if "comp_result" in st.session_state:
        r = st.session_state["comp_result"]
        st.markdown("---")
        oc = r.get("overall_compliance","partial")
        msgs = {"compliant":"✅ Fully compliant with applicable laws.",
                "partial":"⚠️ Partial compliance — some areas need attention.",
                "non_compliant":"❌ Non-compliant — immediate action required."}
        overall_banner(oc, msgs)

        findings = r.get("compliance_findings",[])
        nc_f = [f for f in findings if f.get("status")=="non_compliant"]
        rev_f = [f for f in findings if f.get("status")=="needs_review"]
        ok_f  = [f for f in findings if f.get("status")=="compliant"]

        for label, items, itype in [
            (f"❌ Non-compliant ({len(nc_f)})", nc_f, "error"),
            (f"⚠️ Needs review ({len(rev_f)})", rev_f, "warning"),
            (f"✅ Compliant ({len(ok_f)})", ok_f, "ok"),
        ]:
            if items:
                with st.expander(label, expanded=(itype=="error")):
                    for f in items:
                        issue_card(
                            f"**{f.get('law','')} {f.get('section','')}** — {f.get('finding','')}",
                            itype, f.get("hi",""),
                            f"Action: {f.get('action_required','')} | Risk: {f.get('penalty_risk','')}")

        imm = r.get("immediate_actions",[])
        if imm:
            with st.expander(f"🚨 Immediate actions ({len(imm)})", expanded=True):
                for a in imm:
                    u = a.get("urgency","within_30_days")
                    emoji = {"immediate":"🔴","within_30_days":"🟡","within_90_days":"🟢"}.get(u,"🟡")
                    st.markdown(f"{emoji} **{a.get('action','')}** — {u.replace('_',' ')}")

        periodic = r.get("periodic_compliances",[])
        if periodic:
            with st.expander(f"📅 Periodic compliances ({len(periodic)})"):
                for p in periodic:
                    st.markdown(f"- **{p.get('compliance','')}** — {p.get('frequency','')} | Next: {p.get('due_date','—')}")

        licenses = r.get("licenses_permits",[])
        if licenses:
            with st.expander(f"📋 Licenses & permits ({len(licenses)})"):
                for lic in licenses:
                    s = lic.get("status","missing")
                    emoji = {"valid":"✅","expired":"❌","missing":"⚠️"}.get(s,"⚠️")
                    st.markdown(f"{emoji} **{lic.get('item','')}** — {s} | Renewal: {lic.get('renewal_date','—')}")


# ══════════════════════════════════════════════════════════════════════════════
# P08 — BILLING & ADMIN
# ══════════════════════════════════════════════════════════════════════════════
def render_billing():
    page_header("Billing & Admin", "बिलिंग और प्रशासन", "बिलिंग आणि प्रशासन")

    col1,col2 = st.columns(2)
    with col1:
        billing_type = st.selectbox("Document type", ["Invoice","Fee Note",
            "Retainer Agreement","Engagement Letter","Acknowledgement Receipt",
            "Time Sheet Summary"], key="bill_type")
    with col2:
        lang = lang_selector("bill_lang")

    bc1,bc2,bc3 = st.columns(3)
    with bc1: client_name = st.text_input(t("client_name"), key="bill_client")
    with bc2: advocate_name = st.text_input(t("advocate_name"), key="bill_adv")
    with bc3: st.text_input(t("gst_no"), key="bill_gst", placeholder="27AABCU9603R1ZX")

    matter = st.text_area(t("matter"), height=100,
        placeholder="e.g. Appearing in Bombay High Court WP 1234/2025 — challenge to income tax assessment order",
        key="bill_matter")

    time_entries = st.text_area(t("time_entries"), height=120,
        placeholder="e.g.\n- 2h — Drafting writ petition\n- 1h — Client conference call\n"
                   "- 0.5h — Filing court fee and documents\n- 3h — Hearing appearance",
        key="bill_entries")

    if run_button(t("btn_billing"), t("btn_billing"),"bill_run",disabled=not matter.strip()):
        with st.spinner(t("spinner_analysing")):
            try:
                st.session_state["bill_result"] = generate_billing(
                    matter, time_entries, client_name, advocate_name, billing_type, lang)
            except Exception as e:
                st.error(f"Error: {e}")

    if "bill_result" in st.session_state:
        r = st.session_state["bill_result"]
        st.markdown("---")

        m1,m2,m3 = st.columns(3)
        m1.metric("Subtotal", f"₹{r.get('subtotal',0):,}")
        m2.metric("GST (18%)", f"₹{r.get('gst_18_percent',0):,}")
        m3.metric("Total", f"₹{r.get('total',0):,}")

        if r.get("total_in_words"):
            st.info(f"**{r['total_in_words']}**")

        with st.expander("📋 Line items"):
            items = r.get("line_items",[])
            if items:
                for item in items:
                    st.markdown(f"- **{item.get('description','')}** — "
                                f"{item.get('hours',0)}h × ₹{item.get('rate',0):,} = ₹{item.get('amount',0):,}")

        invoice_text = r.get("formatted_invoice","")
        if invoice_text:
            edited = copy_text_area(invoice_text, "bill_edit", 400, "📄 Invoice (editable)")
            download_text(edited, "invoice.txt", "⬇️ Download invoice")

        time_descs = r.get("time_entry_descriptions",[])
        if time_descs:
            with st.expander("⏱️ Professional time entry descriptions"):
                for td in time_descs: st.markdown(f"- {td}")


# ══════════════════════════════════════════════════════════════════════════════
# P09 — COURT FILING PREP
# ══════════════════════════════════════════════════════════════════════════════
def render_court_filing():
    from data.courts import COURTS, DOCUMENT_TYPES, STATES
    from core.language import detect_language, get_script_note
    from core.pdf_reader import get_word_count
    from ui.results import render_all_results

    page_header("Court Filing Prep", "न्यायालय दाखिल तैयारी", "न्यायालय दाखल तयारी")

    # ── Configuration ──────────────────────────────────────────────────────────
    with st.expander(t("exp_filing_config"), expanded=True):

        # Row 1: Court category → Court name (cascading)
        row1_col1, row1_col2, row1_col3 = st.columns(3)

        with row1_col1:
            court_categories = ["— Select category —"] + list(COURTS.keys())
            sel_category = st.selectbox(
                "Court category",
                options=court_categories,
                key="cf_court_cat",
            )

        with row1_col2:
            # Only show courts from selected category
            if sel_category and not sel_category.startswith("—"):
                courts_in_cat = COURTS[sel_category]
                court_opts = ["— Select court —"] + courts_in_cat
            else:
                court_opts = ["— Select category first —"]
            sel_court = st.selectbox(
                "Court / न्यायालय",
                options=court_opts,
                key="cf_court",
            )
            court = "" if (sel_court.startswith("—")) else sel_court

        with row1_col3:
            state_opts = ["— Select state —"] + STATES
            sel_state = st.selectbox(
                "State / राज्य",
                options=state_opts,
                key="cf_state",
            )
            state = "" if sel_state.startswith("—") else sel_state

        # Row 2: Document category → Document type (cascading)
        row2_col1, row2_col2, row2_col3 = st.columns(3)

        with row2_col1:
            doc_categories = ["— Select category —"] + list(DOCUMENT_TYPES.keys())
            sel_doc_cat = st.selectbox(
                "Document category",
                options=doc_categories,
                key="cf_doc_cat",
            )

        with row2_col2:
            if sel_doc_cat and not sel_doc_cat.startswith("—"):
                types_in_cat = DOCUMENT_TYPES[sel_doc_cat]
                doc_opts = ["— Select type —"] + types_in_cat
            else:
                doc_opts = ["— Select category first —"]
            sel_doc = st.selectbox(
                "Document type / दस्तावेज़ प्रकार",
                options=doc_opts,
                key="cf_doctype",
            )
            doc_type = "" if sel_doc.startswith("—") else sel_doc

        with row2_col3:
            st.markdown("")  # spacer
            st.markdown("")  # spacer
            st.markdown("")  # spacer

        # Confirmation strip — show what's selected
        selected_parts = []
        if court:    selected_parts.append(f"🏛️ {court}")
        if doc_type: selected_parts.append(f"📄 {doc_type}")
        if state:    selected_parts.append(f"📍 {state}")
        if selected_parts:
            st.success("  ·  ".join(selected_parts))
        else:
            st.info("Select court category → court → document category → document type above.")

        # Options toggles
        opt1, opt2 = st.columns(2)
        with opt1:
            translate = st.toggle(
                "Show Hindi translations / हिंदी अनुवाद",
                key="cf_translate",
                help="Each issue and checklist item will include a Hindi translation",
            )
        with opt2:
            flag_mr = st.toggle(
                "Marathi formatting check / मराठी जाँच",
                key="cf_marathi",
                help="Enable Bombay HC Marathi pleading norms check",
            )

    # ── Document input ──────────────────────────────────────────────────────────
    doc_text = doc_input_tabs(
        "cf",
        placeholder=(
            "Paste your court document here...\n\n"
            "यहाँ अपना न्यायालय दस्तावेज़ पेस्ट करें...\n\n"
            "येथे तुमचे न्यायालय दस्तावेज पेस्ट करा..."
        )
    )

    if doc_text.strip():
        lang = detect_language(doc_text)
        st.markdown(
            f"<div class='lang-detected-box'>🌐 {get_script_note(lang)} "
            f"· {get_word_count(doc_text):,} words</div>",
            unsafe_allow_html=True,
        )

    if run_button(t("btn_filing"), t("btn_filing"), "cf_run",
                  disabled=not doc_text.strip()):
        lang_info = detect_language(doc_text) if doc_text else {}
        with st.spinner(t("spinner_filing")):
            try:
                result = prepare_court_filing(
                    doc_text, court, doc_type, state,
                    translate, lang_info.get("label", "Unknown")
                )
                st.session_state["cf_result"] = result
                st.session_state["cf_doc_text"] = doc_text
                st.session_state["cf_config"] = {
                    "court": court, "doc_type": doc_type, "state": state
                }
            except Exception as e:
                st.error(f"Error: {e}")

    if "cf_result" in st.session_state:
        cfg = st.session_state.get("cf_config", {})
        st.markdown("---")
        # Show what was checked
        if cfg.get("court") or cfg.get("doc_type"):
            st.markdown(
                f"<div class='lang-detected-box'>"
                f"{'🏛️ ' + cfg['court'] if cfg.get('court') else ''}"
                f"{'  ·  📄 ' + cfg['doc_type'] if cfg.get('doc_type') else ''}"
                f"{'  ·  📍 ' + cfg['state'] if cfg.get('state') else ''}"
                f"</div>",
                unsafe_allow_html=True,
            )
        render_all_results(st.session_state["cf_result"])

        # ── Download the document as formatted .docx ───────────────────────────
        cf_doc_text = st.session_state.get("cf_doc_text", "")
        if cf_doc_text:
            from ui.docx_download import render_docx_download
            render_docx_download(
                draft_text=cf_doc_text,
                court=cfg.get("court", ""),
                doc_type=cfg.get("doc_type", ""),
                state=cfg.get("state", ""),
                key_prefix="cf",
            )


# ══════════════════════════════════════════════════════════════════════════════
# P10 — MEETING NOTES & DEBRIEF
# ══════════════════════════════════════════════════════════════════════════════
def render_meeting_notes():
    page_header("Meeting Notes & Debrief", "बैठक नोट्स और डीब्रीफ", "बैठक नोंदी")

    col1,col2,col3 = st.columns(3)
    with col1:
        mt = st.selectbox(t("meeting_type"), ["Client meeting","Court hearing debrief",
            "Opposing counsel meeting","Internal team meeting",
            "Settlement negotiation","Arbitration session","Zoom/Video call"], key="mn_type")
    with col2:
        attendees = st.text_input(t("attendees"), key="mn_att",
            placeholder="e.g. Client, Adv. Sharma, Junior")
    with col3:
        lang = lang_selector("mn_lang")

    notes_text = st.text_area(t("notes"),height=220,
        placeholder="Paste meeting notes, audio transcript, or handwritten notes here...\n\n"
                   "Can be rough notes — Claude will structure them.\n\n"
                   "Example:\nmet client today re: property case. he says he has receipts "
                   "from 2018. need to get them by friday. court date is 20 may. "
                   "opposing party wants settlement at 15L, client says minimum 25L. "
                   "need to draft reply affidavit next week.",
        key="mn_notes")

    if run_button(t("btn_meeting"), t("btn_meeting"),"mn_run",disabled=not notes_text.strip()):
        with st.spinner(t("spinner_analysing")):
            try:
                st.session_state["mn_result"] = process_meeting_notes(notes_text, mt, attendees, lang)
            except Exception as e:
                st.error(f"Error: {e}")

    if "mn_result" in st.session_state:
        r = st.session_state["mn_result"]
        st.markdown("---")

        st.markdown(f"<div class='result-card'>"
                    f"<div class='result-card-title'>{r.get('meeting_type','Meeting')} "
                    f"{'— ' + r.get('date_detected','') if r.get('date_detected') else ''}</div>"
                    f"<div style='margin-top:6px;'>{r.get('executive_summary','')}</div>"
                    f"</div>", unsafe_allow_html=True)

        if r.get("hi_summary"):
            st.markdown(f"<div class='lang-detected-box'><span style='font-family:\"Tiro Devanagari Hindi\",serif;'>"
                        f"🇮🇳 {r['hi_summary']}</span></div>", unsafe_allow_html=True)

        actions = r.get("action_items",[])
        with st.expander(f"✅ Action items ({len(actions)})", expanded=True):
            high_a = [a for a in actions if a.get("priority")=="high"]
            other_a = [a for a in actions if a.get("priority")!="high"]
            for a in high_a + other_a:
                p = a.get("priority","medium")
                emoji = {"high":"🔴","medium":"🟡","low":"🟢"}.get(p,"🟡")
                st.markdown(f"{emoji} **{a.get('task','')}** — Owner: {a.get('owner','—')} | By: {a.get('deadline','—')}")

        discussions = r.get("key_discussions",[])
        with st.expander(f"💬 Key discussions ({len(discussions)})"):
            for d in discussions:
                issue_card(f"**{d.get('topic','')}** — {d.get('discussion','')}",
                           "info", sub_text=f"Outcome: {d.get('outcome','')}")

        legal_issues = r.get("legal_issues_raised",[])
        if legal_issues:
            with st.expander(f"⚖️ Legal issues raised ({len(legal_issues)})"):
                for li in legal_issues:
                    issue_card(f"**{li.get('issue','')}** — {li.get('current_status','')}",
                               "warning", sub_text=f"Next step: {li.get('next_step','')}")

        with st.expander("📄 Case note for file", expanded=False):
            case_note = r.get("case_notes","")
            edited_cn = copy_text_area(case_note, "mn_casenote_edit", 200)
            download_text(edited_cn, "case-note.txt", "⬇️ Save case note")


# ══════════════════════════════════════════════════════════════════════════════
# P11 — IP & PATENT SUPPORT
# ══════════════════════════════════════════════════════════════════════════════
def render_ip_patent():
    page_header("IP & Patent Support", "बौद्धिक संपदा सहायता", "बौद्धिक संपदा सहाय्य")

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        ip_type = st.selectbox(t("ip_type"), ["Patent","Trade Mark","Copyright",
            "Design","Trade Secret","Geographical Indication"], key="ip_type")
    with col2:
        task = st.selectbox(t("task"), ["Patentability analysis","Claims drafting/review",
            "Infringement analysis","Filing requirements",
            "Opposition/Objection","Assignment/License review",
            "Prior art search guidance","General advice"], key="ip_task")
    with col3:
        applicant = st.text_input(t("applicant"), key="ip_app")
    with col4:
        lang = lang_selector("ip_lang")

    doc_text = doc_input_tabs("ip", placeholder="Paste patent application, claims, or IP document here...")

    if run_button(f"🔬  Analyse {ip_type}","IP विश्लेषण","ip_run",disabled=not doc_text.strip()):
        with st.spinner(f"Analysing {ip_type} under Indian IP law..."):
            try:
                st.session_state["ip_result"] = support_ip_patent(doc_text, ip_type, task, applicant, lang)
            except Exception as e:
                st.error(f"Error: {e}")

    if "ip_result" in st.session_state:
        r = st.session_state["ip_result"]
        st.markdown("---")

        st.markdown(f"<div class='result-card'><div class='result-card-title'>"
                    f"{r.get('ip_type','')} — {r.get('task','')}</div>"
                    f"<div style='margin-top:6px;'>{r.get('summary','')}</div>"
                    f"</div>", unsafe_allow_html=True)

        # Patentability (only for patents)
        pat = r.get("patentability_assessment",{})
        if pat.get("novelty") or pat.get("inventive_step"):
            with st.expander("🔬 Patentability assessment", expanded=True):
                p1,p2,p3 = st.columns(3)
                with p1: st.metric("Novelty", pat.get("novelty","—")[:20] if pat.get("novelty") else "—")
                with p2: st.metric("Inventive step", pat.get("inventive_step","—")[:20] if pat.get("inventive_step") else "—")
                with p3: st.metric("Industrial app.", pat.get("industrial_applicability","—")[:20] if pat.get("industrial_applicability") else "—")
                for concern in pat.get("prior_art_concerns",[]):
                    issue_card(concern, "warning")

        claims = r.get("claims_analysis",[])
        if claims:
            with st.expander(f"📋 Claims analysis ({len(claims)})", expanded=True):
                for c in claims:
                    strength = c.get("assessment","moderate")
                    issue_card(f"**Claim {c.get('claim_number','')}** [{c.get('type','')}]",
                               {"strong":"ok","moderate":"warning","weak":"error"}.get(strength,"warning"),
                               sub_text=c.get("suggestion",""))

        timeline = r.get("timeline",[])
        with st.expander(f"📅 IPO procedure & timeline ({len(timeline)})"):
            if r.get("ipo_procedure"):
                st.write(r["ipo_procedure"])
            for t in timeline:
                deadline_row(t.get("deadline","—"), t.get("action",""), t.get("stage",""))

        risks = r.get("risks",[])
        if risks:
            with st.expander(f"⚠️ Risks ({len(risks)})"):
                for risk in risks:
                    issue_card(risk.get("risk",""),
                               {"high":"error","medium":"warning","low":"info"}.get(risk.get("severity","medium"),"warning"),
                               sub_text=risk.get("mitigation",""))

        india_notes = r.get("india_specific_notes",[])
        if india_notes:
            with st.expander("🇮🇳 India-specific notes"):
                for n in india_notes: st.markdown(f"- {n.get('note','')}")

        recs = r.get("recommendations",[])
        if recs:
            with st.expander("📌 Recommendations"):
                for rec in recs: st.markdown(f"- {rec}")
        if r.get("estimated_cost"):
            st.info(f"💰 Estimated cost: {r['estimated_cost']}")


# ══════════════════════════════════════════════════════════════════════════════
# P12 — KNOWLEDGE MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
def render_knowledge():
    page_header("Knowledge Management", "ज्ञान प्रबंधन", "ज्ञान व्यवस्थापन")

    col1,col2 = st.columns([2,1])
    with col1:
        area = st.selectbox("Area of law", ["General Indian law","Constitutional Law",
            "Civil Procedure (CPC)","Criminal Law (IPC/CrPC)","Contract Law",
            "Property Law","Family Law","Corporate Law","Tax Law","Labour Law",
            "IP Law","Consumer Law","Banking Law","Arbitration","Service Law",
            "RERA","FEMA","GST","Insolvency (IBC)","POSH Act"], key="km_area")
    with col2:
        lang = lang_selector("km_lang")

    query = st.text_area("Your legal question",height=100,
        placeholder="Ask anything about Indian law...\n\n"
                   "Examples:\n"
                   "• What is the limitation period for recovery of money in India?\n"
                   "• What are the mandatory clauses in a commercial lease agreement?\n"
                   "• How does Section 9 arbitration interim relief work?\n"
                   "• परिसीमा अधिनियम के तहत मुकदमे की अवधि क्या है?",
        key="km_query")

    with st.expander("📎 Add context documents (optional)"):
        context_text = doc_input_tabs("km_ctx", height=120,
            placeholder="Paste any relevant document for context...")

    if run_button(t("btn_knowledge"), t("btn_knowledge"),"km_run",disabled=not query.strip()):
        with st.spinner(t("spinner_analysing")):
            try:
                st.session_state["km_result"] = knowledge_query(query, context_text, area, lang)
            except Exception as e:
                st.error(f"Error: {e}")

    if "km_result" in st.session_state:
        r = st.session_state["km_result"]
        st.markdown("---")

        # Direct answer
        st.markdown(f"<div class='result-card'>"
                    f"<div class='result-card-title' style='font-size:1rem;'>{r.get('query','')}</div>"
                    f"<div style='margin-top:8px;font-size:1rem;line-height:1.7;'>{r.get('direct_answer','')}</div>"
                    f"</div>", unsafe_allow_html=True)

        # Hindi + Marathi always shown
        lang_col1, lang_col2 = st.columns(2)
        with lang_col1:
            if r.get("hi_answer"):
                st.markdown(f"<div class='lang-detected-box'>"
                            f"<span style='font-family:\"Tiro Devanagari Hindi\",serif;'>🇮🇳 {r['hi_answer']}</span>"
                            f"</div>", unsafe_allow_html=True)
        with lang_col2:
            if r.get("mr_answer"):
                st.markdown(f"<div class='lang-detected-box'>"
                            f"<span style='font-family:\"Tiro Devanagari Hindi\",serif;'>🟠 {r['mr_answer']}</span>"
                            f"</div>", unsafe_allow_html=True)

        with st.expander("📖 Detailed explanation", expanded=True):
            st.write(r.get("detailed_explanation",""))

        law_col, case_col = st.columns(2)
        laws = r.get("applicable_laws",[])
        with law_col:
            with st.expander(f"📚 Applicable laws ({len(laws)})"):
                for l in laws:
                    issue_card(f"**{l.get('law','')} — {l.get('section','')}**",
                               "info", sub_text=l.get("text_summary",""))

        cases = r.get("landmark_cases",[])
        with case_col:
            with st.expander(f"⚖️ Landmark cases ({len(cases)})"):
                for c in cases:
                    issue_card(f"**{c.get('case','')}**",
                               "ok", sub_text=c.get("principle",""))

        clauses = r.get("standard_clauses",[])
        if clauses:
            with st.expander(f"📝 Standard clauses ({len(clauses)})"):
                for cl in clauses:
                    st.markdown(f"```\n{cl}\n```")

        mistakes = r.get("common_mistakes",[])
        if mistakes:
            with st.expander(f"⚠️ Common mistakes to avoid ({len(mistakes)})"):
                for m in mistakes: issue_card(m, "warning")

        if r.get("recent_developments"):
            with st.expander("📰 Recent developments"):
                st.write(r["recent_developments"])

        cross_refs = r.get("cross_references",[])
        if cross_refs:
            st.markdown("**Related topics:** " + " · ".join(f"`{c}`" for c in cross_refs))
