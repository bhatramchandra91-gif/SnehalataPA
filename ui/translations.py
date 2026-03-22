"""
ui/translations.py
All UI string translations for English, Hindi (हिंदी), Marathi (मराठी).
Call t("key") anywhere to get the string in the active UI language.
"""
import streamlit as st

# ── Full translation table ────────────────────────────────────────────────────
TRANSLATIONS = {

    # ── App-level ──────────────────────────────────────────────────────────────
    "app_title":            {"en": "Nyay Prep",               "hi": "न्याय प्रेप",            "mr": "न्याय प्रेप"},
    "app_subtitle":         {"en": "Indian Legal Assistant",  "hi": "भारतीय विधिक सहायक",    "mr": "भारतीय कायदेशीर सहाय्यक"},
    "tools_heading":        {"en": "Tools",                   "hi": "उपकरण",                  "mr": "साधने"},
    "info_heading":         {"en": "Info",                    "hi": "जानकारी",                "mr": "माहिती"},
    "ui_language":          {"en": "Interface language",      "hi": "इंटरफ़ेस भाषा",          "mr": "इंटरफेस भाषा"},

    # ── Tool names ─────────────────────────────────────────────────────────────
    "tool_drafting":        {"en": "Document Drafting",       "hi": "दस्तावेज़ मसौदा",        "mr": "दस्तावेज मसुदा"},
    "tool_research":        {"en": "Legal Research",          "hi": "विधिक अनुसंधान",         "mr": "कायदेशीर संशोधन"},
    "tool_contract":        {"en": "Contract Review",         "hi": "अनुबंध समीक्षा",         "mr": "करार पुनरावलोकन"},
    "tool_client_comm":     {"en": "Client Communication",    "hi": "मुवक्किल संचार",         "mr": "अशील संपर्क"},
    "tool_due_diligence":   {"en": "Due Diligence",           "hi": "उचित परिश्रम",           "mr": "योग्य परिश्रम"},
    "tool_discovery":       {"en": "Discovery Support",       "hi": "खोज सहायता",             "mr": "शोध सहाय्य"},
    "tool_compliance":      {"en": "Compliance Checks",       "hi": "अनुपालन जाँच",           "mr": "अनुपालन तपासणी"},
    "tool_billing":         {"en": "Billing & Admin",         "hi": "बिलिंग और प्रशासन",      "mr": "बिलिंग आणि प्रशासन"},
    "tool_court_filing":    {"en": "Court Filing Prep",       "hi": "दाखिल तैयारी",           "mr": "दाखल तयारी"},
    "tool_meeting_notes":   {"en": "Meeting Notes & Debrief", "hi": "बैठक नोट्स",             "mr": "बैठक नोंदी"},
    "tool_ip_patent":       {"en": "IP & Patent Support",     "hi": "बौद्धिक संपदा",          "mr": "बौद्धिक संपदा"},
    "tool_knowledge":       {"en": "Knowledge Management",    "hi": "ज्ञान प्रबंधन",          "mr": "ज्ञान व्यवस्थापन"},

    # ── Common labels ──────────────────────────────────────────────────────────
    "court_category":       {"en": "Court category",          "hi": "न्यायालय श्रेणी",        "mr": "न्यायालय प्रकार"},
    "court":                {"en": "Court",                   "hi": "न्यायालय",               "mr": "न्यायालय"},
    "state":                {"en": "State",                   "hi": "राज्य",                  "mr": "राज्य"},
    "doc_category":         {"en": "Document category",       "hi": "दस्तावेज़ श्रेणी",       "mr": "दस्तावेज प्रकार"},
    "doc_type":             {"en": "Document type",           "hi": "दस्तावेज़ प्रकार",       "mr": "दस्तावेज प्रकार"},
    "output_language":      {"en": "Output language",         "hi": "आउटपुट भाषा",            "mr": "आउटपुट भाषा"},
    "parties":              {"en": "Parties",                 "hi": "पक्षकार",                "mr": "पक्षकार"},
    "facts":                {"en": "Facts / Instructions",    "hi": "तथ्य / निर्देश",         "mr": "तथ्य / सूचना"},
    "client_name":          {"en": "Client name",             "hi": "मुवक्किल का नाम",        "mr": "अशीलाचे नाव"},
    "advocate_name":        {"en": "Advocate / Firm",         "hi": "अधिवक्ता / फर्म",        "mr": "वकील / फर्म"},
    "case_ref":             {"en": "Case reference",          "hi": "मामला संदर्भ",           "mr": "प्रकरण संदर्भ"},
    "question":             {"en": "Research question",       "hi": "शोध प्रश्न",             "mr": "संशोधन प्रश्न"},
    "area_of_law":          {"en": "Area of law",             "hi": "कानून का क्षेत्र",       "mr": "कायद्याचे क्षेत्र"},
    "meeting_type":         {"en": "Meeting type",            "hi": "बैठक प्रकार",            "mr": "बैठकीचा प्रकार"},
    "attendees":            {"en": "Attendees",               "hi": "उपस्थित लोग",            "mr": "उपस्थित लोक"},
    "notes":                {"en": "Notes / Transcript",      "hi": "नोट्स / प्रतिलिपि",     "mr": "नोंदी / प्रतिलिपी"},
    "matter":               {"en": "Matter description",      "hi": "मामले का विवरण",         "mr": "प्रकरणाचे वर्णन"},
    "time_entries":         {"en": "Time entries",            "hi": "समय प्रविष्टियाँ",       "mr": "वेळ नोंदी"},
    "industry":             {"en": "Industry",                "hi": "उद्योग",                 "mr": "उद्योग"},
    "entity_type":          {"en": "Entity type",             "hi": "इकाई प्रकार",            "mr": "संस्था प्रकार"},
    "case_type":            {"en": "Case type",               "hi": "मामला प्रकार",           "mr": "प्रकरण प्रकार"},
    "transaction":          {"en": "Transaction / matter",    "hi": "लेनदेन / मामला",         "mr": "व्यवहार / प्रकरण"},
    "ip_type":              {"en": "IP type",                 "hi": "आईपी प्रकार",            "mr": "आयपी प्रकार"},
    "task":                 {"en": "Task",                    "hi": "कार्य",                  "mr": "काम"},
    "applicant":            {"en": "Applicant / Client",      "hi": "आवेदक / मुवक्किल",      "mr": "अर्जदार / अशील"},
    "governing_law":        {"en": "Governing law",           "hi": "शासी कानून",             "mr": "नियामक कायदा"},
    "client_role":          {"en": "Client is",               "hi": "मुवक्किल हैं",           "mr": "अशील आहे"},
    "contract_type":        {"en": "Contract type",           "hi": "अनुबंध प्रकार",          "mr": "करार प्रकार"},
    "comm_type":            {"en": "Communication type",      "hi": "संचार प्रकार",           "mr": "संपर्क प्रकार"},
    "purpose":              {"en": "Purpose",                 "hi": "उद्देश्य",               "mr": "उद्देश"},
    "tone":                 {"en": "Tone",                    "hi": "शैली",                   "mr": "शैली"},
    "case_notes":           {"en": "Case notes / update",     "hi": "मामले के नोट्स",         "mr": "प्रकरण नोंदी"},
    "specific_laws":        {"en": "Specific laws to check",  "hi": "जाँच के लिए कानून",      "mr": "तपासण्यासाठी कायदे"},
    "filing_config":        {"en": "Filing configuration",    "hi": "दाखिल विन्यास",          "mr": "दाखल सेटिंग"},
    "hindi_translation":    {"en": "Show Hindi translations", "hi": "हिंदी अनुवाद दिखाएँ",   "mr": "हिंदी भाषांतर दाखवा"},
    "marathi_check":        {"en": "Marathi formatting check","hi": "मराठी जाँच",             "mr": "मराठी तपासणी"},
    "context_docs":         {"en": "Context documents",       "hi": "संदर्भ दस्तावेज़",       "mr": "संदर्भ दस्तावेज"},
    "billing_type":         {"en": "Document type",           "hi": "दस्तावेज़ प्रकार",       "mr": "दस्तावेज प्रकार"},
    "gst_no":               {"en": "GST No. (optional)",      "hi": "जीएसटी नंबर (वैकल्पिक)","mr": "GST क्रमांक (पर्यायी)"},
    "dd_type":              {"en": "DD type",                 "hi": "डीडी प्रकार",            "mr": "DD प्रकार"},
    "case_summary":         {"en": "Brief case summary",      "hi": "मामले का संक्षिप्त विवरण","mr": "प्रकरणाचा थोडक्यात आढावा"},

    # ── Placeholders ───────────────────────────────────────────────────────────
    "ph_select_category":   {"en": "— Select category —",    "hi": "— श्रेणी चुनें —",       "mr": "— प्रकार निवडा —"},
    "ph_select_court":      {"en": "— Select court —",       "hi": "— न्यायालय चुनें —",     "mr": "— न्यायालय निवडा —"},
    "ph_select_type":       {"en": "— Select type —",        "hi": "— प्रकार चुनें —",       "mr": "— प्रकार निवडा —"},
    "ph_select_state":      {"en": "— Select state —",       "hi": "— राज्य चुनें —",        "mr": "— राज्य निवडा —"},
    "ph_select_first":      {"en": "— Select category first —", "hi": "— पहले श्रेणी चुनें —", "mr": "— आधी प्रकार निवडा —"},
    "ph_parties":           {"en": "e.g. ABC Pvt Ltd (Petitioner) vs State of Maharashtra (Respondent)",
                             "hi": "जैसे: एबीसी प्रा. लि. (याचिकाकर्ता) बनाम महाराष्ट्र राज्य (प्रतिवादी)",
                             "mr": "उदा: ABC प्रा. लि. (याचिकाकर्ता) विरुद्ध महाराष्ट्र राज्य (प्रतिवादी)"},
    "ph_facts":             {"en": "Describe the facts and what you need drafted...",
                             "hi": "तथ्य और क्या मसौदा तैयार करना है वह बताएं...",
                             "mr": "तथ्ये आणि काय मसुदा तयार करायचा ते सांगा..."},
    "ph_question":          {"en": "Ask any Indian law question...",
                             "hi": "कोई भी भारतीय कानून प्रश्न पूछें...",
                             "mr": "कोणताही भारतीय कायदा प्रश्न विचारा..."},
    "ph_case_notes":        {"en": "Describe what happened and what client needs to know...",
                             "hi": "क्या हुआ और मुवक्किल को क्या जानना चाहिए बताएं...",
                             "mr": "काय झाले आणि अशीलाला काय माहित असणे आवश्यक आहे ते सांगा..."},
    "ph_notes":             {"en": "Paste meeting notes or rough transcript here...",
                             "hi": "बैठक नोट्स या प्रतिलिपि यहाँ पेस्ट करें...",
                             "mr": "बैठकीच्या नोंदी किंवा प्रतिलिपी येथे पेस्ट करा..."},
    "ph_matter":            {"en": "e.g. Appearing in Bombay HC WP 1234/2025 — challenge to IT assessment",
                             "hi": "जैसे: बॉम्बे एचसी में WP 1234/2025 में पेश होना",
                             "mr": "उदा: मुंबई HC WP 1234/2025 मध्ये IT मूल्यांकनाला आव्हान"},
    "ph_paste_doc":         {"en": "Paste document text here...",
                             "hi": "दस्तावेज़ पाठ यहाँ पेस्ट करें...",
                             "mr": "दस्तावेज मजकूर येथे पेस्ट करा..."},
    "ph_client":            {"en": "e.g. Ramesh Sharma",      "hi": "जैसे: रमेश शर्मा",      "mr": "उदा: रमेश शर्मा"},
    "ph_advocate":          {"en": "e.g. Adv. Priya Desai",   "hi": "जैसे: अधि. प्रिया देसाई","mr": "उदा: अॅड. प्रिया देसाई"},
    "ph_case_ref":          {"en": "e.g. WP 1234/2025",       "hi": "जैसे: WP 1234/2025",    "mr": "उदा: WP 1234/2025"},

    # ── Button labels ──────────────────────────────────────────────────────────
    "btn_draft":            {"en": "✍️  Draft document",      "hi": "दस्तावेज़ तैयार करें",   "mr": "दस्तावेज तयार करा"},
    "btn_research":         {"en": "🔍  Research",             "hi": "अनुसंधान करें",          "mr": "संशोधन करा"},
    "btn_review_contract":  {"en": "🔍  Review contract",      "hi": "अनुबंध जाँचें",          "mr": "करार तपासा"},
    "btn_draft_comm":       {"en": "✉️  Draft communication", "hi": "संदेश तैयार करें",       "mr": "संदेश तयार करा"},
    "btn_due_diligence":    {"en": "🔎  Run due diligence",    "hi": "DD जाँचें",              "mr": "DD तपासा"},
    "btn_discovery":        {"en": "🔬  Analyse for discovery","hi": "खोज विश्लेषण करें",     "mr": "शोध विश्लेषण करा"},
    "btn_compliance":       {"en": "✅  Check compliance",     "hi": "अनुपालन जाँचें",         "mr": "अनुपालन तपासा"},
    "btn_billing":          {"en": "🧾  Generate billing doc", "hi": "बिल तैयार करें",         "mr": "बिल तयार करा"},
    "btn_filing":           {"en": "⚖️  Run filing checks",   "hi": "दाखिल जाँच करें",        "mr": "दाखल तपासा"},
    "btn_meeting":          {"en": "📝  Process notes",        "hi": "नोट्स तैयार करें",       "mr": "नोंदी तयार करा"},
    "btn_ip":               {"en": "🔬  Analyse IP",           "hi": "IP विश्लेषण करें",       "mr": "IP विश्लेषण करा"},
    "btn_knowledge":        {"en": "🧠  Query knowledge base", "hi": "ज्ञान खोजें",            "mr": "ज्ञान शोधा"},
    "btn_clear":            {"en": "🔄 Clear",                 "hi": "साफ करें",               "mr": "साफ करा"},
    "btn_download":         {"en": "⬇️ Download",             "hi": "डाउनलोड करें",           "mr": "डाउनलोड करा"},
    "btn_download_draft":   {"en": "⬇️ Download draft",       "hi": "मसौदा डाउनलोड करें",    "mr": "मसुदा डाउनलोड करा"},
    "btn_download_report":  {"en": "⬇️ Download report",      "hi": "रिपोर्ट डाउनलोड करें",  "mr": "अहवाल डाउनलोड करा"},

    # ── Tabs ───────────────────────────────────────────────────────────────────
    "tab_paste":            {"en": "✏️ Paste text",           "hi": "✏️ पाठ पेस्ट करें",     "mr": "✏️ मजकूर पेस्ट करा"},
    "tab_upload":           {"en": "📎 Upload PDF / DOCX",    "hi": "📎 फ़ाइल अपलोड करें",   "mr": "📎 फाइल अपलोड करा"},
    "tab_primary":          {"en": "📧 Primary draft",        "hi": "📧 मुख्य मसौदा",         "mr": "📧 मुख्य मसुदा"},
    "tab_bilingual":        {"en": "🌐 Hindi / Marathi",      "hi": "🌐 हिंदी / मराठी",      "mr": "🌐 हिंदी / मराठी"},

    # ── Expander titles ────────────────────────────────────────────────────────
    "exp_filing_config":    {"en": "⚙️ Filing configuration", "hi": "⚙️ दाखिल विन्यास",     "mr": "⚙️ दाखल सेटिंग"},
    "exp_placeholders":     {"en": "⚠️ Fill in these placeholders before filing",
                             "hi": "⚠️ दाखिल करने से पहले ये भरें",
                             "mr": "⚠️ दाखल करण्यापूर्वी हे भरा"},
    "exp_summary":          {"en": "📋 Summary",              "hi": "📋 सारांश",              "mr": "📋 सारांश"},
    "exp_action_items":     {"en": "✅ Action items",         "hi": "✅ कार्य सूची",          "mr": "✅ कृती सूची"},
    "exp_key_discussions":  {"en": "💬 Key discussions",      "hi": "💬 मुख्य चर्चाएं",      "mr": "💬 मुख्य चर्चा"},
    "exp_case_note":        {"en": "📄 Case note for file",   "hi": "📄 फ़ाइल के लिए नोट",   "mr": "📄 फाइलसाठी नोंद"},
    "exp_optional_doc":     {"en": "📎 Add context documents (optional)",
                             "hi": "📎 संदर्भ दस्तावेज़ जोड़ें (वैकल्पिक)",
                             "mr": "📎 संदर्भ दस्तावेज जोडा (पर्यायी)"},
    "exp_preview":          {"en": "Preview extracted text",  "hi": "निकाला गया पाठ देखें",  "mr": "काढलेला मजकूर पहा"},

    # ── Status / info messages ─────────────────────────────────────────────────
    "info_select_first":    {"en": "Select court category → court → document category → document type above.",
                             "hi": "ऊपर न्यायालय श्रेणी → न्यायालय → दस्तावेज़ श्रेणी → दस्तावेज़ प्रकार चुनें।",
                             "mr": "वर न्यायालय प्रकार → न्यायालय → दस्तावेज प्रकार → दस्तावेज निवडा।"},
    "info_paste_any_lang":  {"en": "Paste document in English, Hindi, or Marathi — language is auto-detected.",
                             "hi": "दस्तावेज़ अंग्रेज़ी, हिंदी या मराठी में पेस्ट करें — भाषा स्वतः पहचानी जाएगी।",
                             "mr": "दस्तावेज इंग्रजी, हिंदी किंवा मराठीत पेस्ट करा — भाषा आपोआप ओळखली जाईल।"},
    "spinner_analysing":    {"en": "Analysing...",            "hi": "विश्लेषण हो रहा है...", "mr": "विश्लेषण होत आहे..."},
    "spinner_drafting":     {"en": "Drafting document...",    "hi": "दस्तावेज़ तैयार हो रहा है...", "mr": "दस्तावेज तयार होत आहे..."},
    "spinner_filing":       {"en": "Analysing filing...",     "hi": "दाखिल जाँच हो रही है...","mr": "दाखल तपासणी होत आहे..."},
    "lbl_document":         {"en": "Document:",              "hi": "दस्तावेज़:",              "mr": "दस्तावेज:"},
    "lbl_court_out":        {"en": "Court:",                 "hi": "न्यायालय:",               "mr": "न्यायालय:"},
    "lbl_sections":         {"en": "Sections:",              "hi": "खंड:",                    "mr": "विभाग:"},
    "lbl_edited_draft":     {"en": "📄 Drafted document *(editable)*",
                             "hi": "📄 तैयार दस्तावेज़ *(संपादन योग्य)*",
                             "mr": "📄 तयार दस्तावेज *(संपादन करण्यायोग्य)*"},
}


def get_ui_lang() -> str:
    """Return the current UI language code: 'en', 'hi', or 'mr'."""
    return st.session_state.get("ui_lang", "en")


def t(key: str) -> str:
    """Translate a key to the current UI language. Falls back to English."""
    lang = get_ui_lang()
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang) or entry.get("en") or key


def render_lang_switcher():
    """
    Render the 3-button language switcher in the sidebar.
    Stores selection in st.session_state['ui_lang'].
    """
    if "ui_lang" not in st.session_state:
        st.session_state["ui_lang"] = "en"

    current = st.session_state["ui_lang"]

    st.markdown(
        f"<div class='sidebar-section-title'>{t('ui_language')}</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        active = current == "en"
        if st.button(
            "EN" if not active else "✓ EN",
            key="lang_en",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state["ui_lang"] = "en"
            st.rerun()

    with col2:
        active = current == "hi"
        if st.button(
            "हिंदी" if not active else "✓ हिंदी",
            key="lang_hi",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state["ui_lang"] = "hi"
            st.rerun()

    with col3:
        active = current == "mr"
        if st.button(
            "मराठी" if not active else "✓ मराठी",
            key="lang_mr",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state["ui_lang"] = "mr"
            st.rerun()
