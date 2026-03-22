"""
core/tools.py
All 12 legal tool analyzers. Each returns a structured dict via Claude.
"""
from core.claude_client import call_claude, call_claude_json
from core.pdf_reader import truncate_for_api

INDIAN_LAW_SYSTEM = """You are a senior Indian advocate and legal assistant with expertise in:
- CPC 1908, CrPC 1973, IPC 1860, Indian Evidence Act 1872
- Indian Contract Act 1872, Specific Relief Act 1963
- Companies Act 2013, Arbitration & Conciliation Act 1996
- Constitutional law, High Court Rules, Supreme Court Rules 2013
- DPDP Act 2023, IT Act 2000, Consumer Protection Act 2019
- Bombay High Court Rules, Maharashtra civil & criminal procedure
Documents may be in English, Hindi (हिंदी), or Marathi (मराठी). Understand all three natively."""


# ── 1. DOCUMENT DRAFTING ──────────────────────────────────────────────────────
def draft_document(doc_type: str, facts: str, court: str, party_details: str,
                   language: str = "English") -> dict:
    lang_note = {
        "Hindi": "Draft entirely in formal Hindi (हिंदी) suitable for Indian courts.",
        "Marathi": "Draft entirely in formal Marathi (मराठी) suitable for Maharashtra courts.",
    }.get(language, "Draft in English.")

    prompt = f"""Draft a complete Indian court/legal document.
{lang_note}

Return ONLY valid JSON:
{{
  "title": "Document title",
  "document": "Full drafted document text with all standard sections",
  "sections_included": ["list of sections included"],
  "notes": ["Any important notes or missing info the lawyer should fill in"],
  "word_count": 0
}}

Document type: {doc_type}
Court / Jurisdiction: {court or "Not specified"}
Party details: {party_details or "Not specified"}
Facts / Instructions:
{facts}

Draft a complete, professional document following Indian legal format:
- Proper cause title and court heading
- Correct party designations per document type
- All mandatory sections (prayer, verification, signature block)
- Standard Indian legal language and phrasing
- Placeholder markers like [___] for missing details"""
    return call_claude_json(prompt, max_tokens=3000, system=INDIAN_LAW_SYSTEM)


# ── 2. LEGAL RESEARCH ─────────────────────────────────────────────────────────
def research_legal_question(question: str, area_of_law: str = "",
                             doc_text: str = "", language: str = "English") -> dict:
    lang_note = "Respond in Hindi." if language == "Hindi" else "Respond in Marathi." if language == "Marathi" else "Respond in English."
    doc_section = f"\nDocument/judgment to analyze:\n---\n{truncate_for_api(doc_text, 5000)}\n---" if doc_text else ""

    prompt = f"""You are researching an Indian legal question. {lang_note}
Return ONLY valid JSON:
{{
  "question_answered": "Restate the question clearly",
  "direct_answer": "Clear, direct answer in 2-3 sentences",
  "detailed_analysis": "Comprehensive analysis",
  "relevant_statutes": [{{"act": "Act name", "section": "Section number", "relevance": "How it applies"}}],
  "key_cases": [{{"case": "Case name and citation", "court": "Court", "year": "Year", "holding": "Key holding", "relevance": "How it applies"}}],
  "practical_advice": ["Practical point 1", "Practical point 2"],
  "limitations": "Important caveats or when this answer may differ",
  "confidence": "high|medium|low",
  "hi_summary": "2-sentence Hindi summary (always include regardless of language setting)"
}}

Area of law: {area_of_law or "Auto-detect"}
Research question: {question}
{doc_section}"""
    return call_claude_json(prompt, max_tokens=2500, system=INDIAN_LAW_SYSTEM)


# ── 3. CONTRACT REVIEW ────────────────────────────────────────────────────────
def review_contract(doc_text: str, contract_type: str = "", party_role: str = "",
                    governing_law: str = "Indian Law", language: str = "English") -> dict:
    prompt = f"""Review this Indian law contract thoroughly.
Return ONLY valid JSON:
{{
  "overall_risk": "low|medium|high",
  "contract_type_detected": "type",
  "governing_law_detected": "law",
  "duration": "term",
  "parties": ["Party 1 name/role", "Party 2 name/role"],
  "contract_summary": "3-sentence summary",
  "risk_clauses": [{{"clause": "name", "risk_level": "high|medium|low", "issue": "problem", "recommendation": "fix", "hi": "हिंदी"}}],
  "missing_clauses": [{{"clause": "name", "importance": "high|medium|low", "reason": "why needed under Indian law"}}],
  "obligations": {{"party1": [{{"text": "obligation", "deadline": "when or null"}}], "party2": [{{"text": "obligation", "deadline": "when or null"}}]}},
  "key_dates": [{{"date": "date", "event": "what", "urgency": "high|med|low"}}],
  "redline_suggestions": [{{"original": "original text", "suggested": "new text", "reason": "why"}}],
  "dpdp_compliance": "Assessment of Digital Personal Data Protection Act 2023 compliance if applicable"
}}

Contract type: {contract_type or "Auto-detect"}
Client role: {party_role or "Analyze both sides"}
Governing law: {governing_law}

CONTRACT:
{truncate_for_api(doc_text)}"""
    return call_claude_json(prompt, max_tokens=2500, system=INDIAN_LAW_SYSTEM)


# ── 4. CLIENT COMMUNICATION ───────────────────────────────────────────────────
def draft_client_communication(update: str, comm_type: str = "Email",
                                client_name: str = "", advocate_name: str = "",
                                case_ref: str = "", tone: str = "Professional",
                                language: str = "English") -> dict:
    lang_map = {
        "Hindi": "Write entirely in formal Hindi (हिंदी). Use आदरणीय/महोदय.",
        "Marathi": "Write entirely in formal Marathi (मराठी). Use आदरणीय महोदय/महोदया.",
        "English + Hindi": "Write each paragraph in English, followed by Hindi translation.",
    }
    lang_note = lang_map.get(language, "Write in professional English.")

    prompt = f"""Draft a professional {comm_type} from an Indian advocate to their client.
{lang_note} Tone: {tone}.
Return ONLY valid JSON:
{{
  "subject": "Subject line",
  "body": "Full {comm_type} body",
  "body_hi": "Hindi/Marathi version if bilingual requested, else null",
  "plain_summary": "2-sentence plain English summary of what this communicates",
  "action_items": ["What client must do", "Documents needed", "Dates to note"],
  "follow_up_date": "When advocate will follow up or null"
}}

Communication type: {comm_type}
Client: {client_name or "Client"}
Advocate: {advocate_name or "Advocate"}
Case reference: {case_ref or "Not specified"}
Case update / notes:
{update}

Rules:
- Be clear, avoid legal jargon the client won't understand
- State next steps explicitly
- For bad news: be empathetic but factual
- Under 300 words for emails, shorter for WhatsApp/SMS"""
    return call_claude_json(prompt, max_tokens=1500, system=INDIAN_LAW_SYSTEM)


# ── 5. DUE DILIGENCE ──────────────────────────────────────────────────────────
def run_due_diligence(doc_text: str, dd_type: str = "Corporate",
                       transaction: str = "", language: str = "English") -> dict:
    prompt = f"""Perform {dd_type} due diligence analysis under Indian law.
Return ONLY valid JSON:
{{
  "dd_type": "{dd_type}",
  "transaction_summary": "What transaction this DD is for",
  "overall_assessment": "clean|minor_issues|significant_issues|deal_breaker",
  "red_flags": [{{"issue": "description", "severity": "high|medium|low", "recommendation": "action", "hi": "हिंदी"}}],
  "green_flags": [{{"item": "positive finding"}}],
  "document_checklist": [{{"document": "doc name", "status": "found|missing|unclear", "importance": "mandatory|important|optional"}}],
  "legal_compliance": [{{"area": "law/regulation", "status": "compliant|non_compliant|needs_review", "notes": "details"}}],
  "financial_legal_risks": ["risk 1", "risk 2"],
  "conditions_precedent": ["Condition that must be met before closing"],
  "recommendations": ["Action 1", "Action 2"],
  "summary_report": "3-paragraph executive summary"
}}

DD type: {dd_type}
Transaction: {transaction or "Not specified"}
DOCUMENT:
{truncate_for_api(doc_text)}"""
    return call_claude_json(prompt, max_tokens=2500, system=INDIAN_LAW_SYSTEM)


# ── 6. DISCOVERY SUPPORT ──────────────────────────────────────────────────────
def support_discovery(doc_text: str, case_type: str = "", case_summary: str = "",
                       task: str = "Full analysis", language: str = "English") -> dict:
    prompt = f"""Assist with litigation discovery/evidence analysis under Indian law (CPC Order XI, Evidence Act).
Return ONLY valid JSON:
{{
  "case_summary_detected": "Brief summary of case from document",
  "key_facts": [{{"fact": "fact statement", "source": "where in doc", "significance": "high|medium|low"}}],
  "timeline": [{{"date": "date", "event": "what happened", "significance": "why it matters"}}],
  "evidence_found": [{{"item": "evidence description", "type": "documentary|oral|electronic|expert", "strength": "strong|moderate|weak", "admissibility_note": "any Indian Evidence Act note"}}],
  "interrogatory_questions": ["Question to ask opposite party under Order XI CPC"],
  "document_requests": ["Documents to request from opposite party"],
  "witness_prep": [{{"witness_type": "role", "key_questions": ["Q1","Q2"], "likely_testimony": "what they would say"}}],
  "weaknesses_in_case": [{{"weakness": "issue", "mitigation": "how to address"}}],
  "strengths_in_case": ["Strength 1", "Strength 2"],
  "recommended_next_steps": ["Step 1", "Step 2"]
}}

Case type: {case_type or "Civil"}
Case summary: {case_summary or "See document"}
Task: {task}
DOCUMENT:
{truncate_for_api(doc_text)}"""
    return call_claude_json(prompt, max_tokens=2500, system=INDIAN_LAW_SYSTEM)


# ── 7. COMPLIANCE CHECKS ──────────────────────────────────────────────────────
def check_compliance(doc_text: str, industry: str = "", company_type: str = "",
                      specific_laws: str = "", language: str = "English") -> dict:
    prompt = f"""Perform a compliance review under applicable Indian laws and regulations.
Return ONLY valid JSON:
{{
  "overall_compliance": "compliant|partial|non_compliant",
  "company_type_detected": "type",
  "applicable_laws": ["List of laws that apply"],
  "compliance_findings": [{{
    "law": "Act/Rule name",
    "section": "specific section",
    "status": "compliant|non_compliant|needs_review",
    "finding": "what was found",
    "action_required": "what to do",
    "deadline": "any statutory deadline",
    "penalty_risk": "penalty if non-compliant",
    "hi": "हिंदी summary"
  }}],
  "immediate_actions": [{{"action": "what to do", "urgency": "immediate|within_30_days|within_90_days"}}],
  "periodic_compliances": [{{"compliance": "what", "frequency": "monthly/quarterly/annual", "due_date": "when"}}],
  "licenses_permits": [{{"item": "license/permit", "status": "valid|expired|missing", "renewal_date": "date or null"}}],
  "summary": "2-paragraph compliance summary"
}}

Industry: {industry or "General"}
Company type: {company_type or "Not specified"}
Specific laws to check: {specific_laws or "All applicable"}
DOCUMENT:
{truncate_for_api(doc_text)}"""
    return call_claude_json(prompt, max_tokens=2500, system=INDIAN_LAW_SYSTEM)


# ── 8. BILLING & ADMIN ────────────────────────────────────────────────────────
def generate_billing(matter_description: str, time_entries: str = "",
                      client_name: str = "", advocate_name: str = "",
                      billing_type: str = "Invoice", language: str = "English") -> dict:
    prompt = f"""Generate professional legal billing documents for an Indian law firm.
Return ONLY valid JSON:
{{
  "document_type": "{billing_type}",
  "invoice_number": "INV-2025-001",
  "client": "{client_name or 'Client'}",
  "advocate": "{advocate_name or 'Advocate'}",
  "matter_summary": "1-sentence description of the legal matter",
  "line_items": [{{"description": "service description", "hours": 0.0, "rate": 0, "amount": 0}}],
  "subtotal": 0,
  "gst_18_percent": 0,
  "total": 0,
  "total_in_words": "Rupees ... Only",
  "payment_terms": "Payment due within 30 days",
  "bank_details_placeholder": "[Add your bank account details here]",
  "notes": ["Any notes about the bill"],
  "time_entry_descriptions": ["Professional time entry description 1", "Professional time entry description 2"],
  "formatted_invoice": "Full formatted invoice text ready to send"
}}

Billing type: {billing_type}
Client: {client_name or "Client"}
Advocate/Firm: {advocate_name or "Advocate"}
Matter description: {matter_description}
Time entries / work done:
{time_entries or "Generate based on matter description"}

Notes:
- Use INR (₹) currency
- Add 18% GST on professional fees (SAC code 998212 for legal services)
- Professional, formal language appropriate for Indian law firms"""
    return call_claude_json(prompt, max_tokens=1500, system=INDIAN_LAW_SYSTEM)


# ── 9. COURT FILING PREP ──────────────────────────────────────────────────────
def prepare_court_filing(doc_text: str, court: str = "", doc_type: str = "",
                          state: str = "", translate_hindi: bool = False,
                          detected_language: str = "English") -> dict:
    translate_note = 'Include "hi" field (Hindi) for each issue and checklist item.' if translate_hindi else 'No "hi" fields needed.'
    prompt = f"""Pre-filing review for Indian court document. {translate_note}
Return ONLY valid JSON:
{{
  "overall": "pass|warn|fail",
  "detectedLanguage": "{detected_language}",
  "format": {{
    "status": "pass|warn|fail",
    "summary": "one sentence",
    "issues": [{{"type": "ok|warning|error|info", "text": "issue", "hi": "हिंदी or null"}}]
  }},
  "exhibits": {{
    "status": "pass|warn|fail",
    "summary": "one sentence",
    "issues": [{{"type": "ok|warning|error|info", "text": "issue", "hi": "हिंदी or null"}}]
  }},
  "checklist": {{
    "status": "pass|warn|fail",
    "summary": "one sentence",
    "items": [{{"text": "item", "hi": "हिंदी or null", "priority": "high|med|low"}}]
  }},
  "deadlines": {{
    "status": "pass|warn|fail",
    "summary": "one sentence",
    "items": [{{"date": "DD/MM/YYYY", "dateType": "Hearing|Limitation|Filing|Response", "description": "what", "hi": "हिंदी or null", "urgency": "high|med|low"}}]
  }}
}}

Court: {court or "Indian court"}
Doc type: {doc_type or "Legal document"}
State: {state or "Not specified"}
DOCUMENT:
{truncate_for_api(doc_text)}"""
    return call_claude_json(prompt, max_tokens=2000, system=INDIAN_LAW_SYSTEM)


# ── 10. MEETING NOTES & DEBRIEF ───────────────────────────────────────────────
def process_meeting_notes(notes_text: str, meeting_type: str = "Client meeting",
                           attendees: str = "", language: str = "English") -> dict:
    prompt = f"""Process legal meeting notes/transcript and create structured debrief.
Return ONLY valid JSON:
{{
  "meeting_type": "{meeting_type}",
  "date_detected": "date from notes or null",
  "attendees_detected": ["list of attendees found in notes"],
  "executive_summary": "3-sentence summary of the meeting",
  "key_discussions": [{{"topic": "topic", "discussion": "what was discussed", "outcome": "decision/conclusion"}}],
  "action_items": [{{"task": "what to do", "owner": "who is responsible", "deadline": "by when", "priority": "high|medium|low"}}],
  "legal_issues_raised": [{{"issue": "legal issue", "current_status": "status", "next_step": "action"}}],
  "client_instructions": ["Instruction from client 1", "Instruction 2"],
  "advice_given": ["Legal advice given 1", "Legal advice given 2"],
  "follow_up_required": [{{"item": "follow-up needed", "by": "who", "when": "deadline"}}],
  "case_notes": "Formal case note paragraph suitable for file recording",
  "next_meeting": "Next meeting date/topic if mentioned or null",
  "hi_summary": "Hindi summary of action items (always include)"
}}

Meeting type: {meeting_type}
Attendees: {attendees or "See notes"}
NOTES/TRANSCRIPT:
{truncate_for_api(notes_text, 6000)}"""
    return call_claude_json(prompt, max_tokens=2000, system=INDIAN_LAW_SYSTEM)


# ── 11. IP & PATENT SUPPORT ───────────────────────────────────────────────────
def support_ip_patent(doc_text: str, ip_type: str = "Patent",
                       task: str = "Analysis", applicant: str = "",
                       language: str = "English") -> dict:
    prompt = f"""Assist with Indian IP law matter under Patents Act 1970, Trade Marks Act 1999,
Copyright Act 1957, Designs Act 2000, GI Act 1999.
Return ONLY valid JSON:
{{
  "ip_type": "{ip_type}",
  "task": "{task}",
  "applicant": "{applicant or 'Not specified'}",
  "summary": "What this IP matter is about",
  "patentability_assessment": {{
    "novelty": "assessment or null if not patent",
    "inventive_step": "assessment or null",
    "industrial_applicability": "assessment or null",
    "prior_art_concerns": ["concern 1", "concern 2"]
  }},
  "claims_analysis": [{{"claim_number": "1", "type": "independent|dependent", "assessment": "strong|moderate|weak", "suggestion": "improvement"}}],
  "filing_requirements": [{{"requirement": "what's needed", "status": "met|missing|unclear"}}],
  "timeline": [{{"stage": "stage name", "deadline": "timeframe", "action": "what to do"}}],
  "risks": [{{"risk": "description", "severity": "high|medium|low", "mitigation": "how to address"}}],
  "india_specific_notes": [{{"note": "India-specific consideration"}}],
  "ipo_procedure": "Relevant Indian Patent Office / Trade Marks Registry procedure",
  "estimated_cost": "Rough cost estimate in INR",
  "recommendations": ["Recommendation 1", "Recommendation 2"]
}}

IP type: {ip_type}
Task: {task}
Applicant: {applicant or "Not specified"}
DOCUMENT:
{truncate_for_api(doc_text)}"""
    return call_claude_json(prompt, max_tokens=2000, system=INDIAN_LAW_SYSTEM)


# ── 12. KNOWLEDGE MANAGEMENT ──────────────────────────────────────────────────
def knowledge_query(query: str, context_docs: str = "",
                     area: str = "", language: str = "English") -> dict:
    lang_note = "Respond in Hindi." if language == "Hindi" else "Respond in Marathi." if language == "Marathi" else "Respond in English."
    prompt = f"""Answer this Indian legal knowledge query comprehensively. {lang_note}
Return ONLY valid JSON:
{{
  "query": "{query}",
  "direct_answer": "Clear, direct answer",
  "detailed_explanation": "Comprehensive explanation with legal basis",
  "applicable_laws": [{{"law": "Act name", "section": "section", "text_summary": "what it says"}}],
  "landmark_cases": [{{"case": "name and citation", "court": "court name", "principle": "legal principle established"}}],
  "standard_clauses": ["Standard clause 1 if relevant", "Standard clause 2"],
  "templates_available": ["Template 1 that exists for this", "Template 2"],
  "common_mistakes": ["Common mistake lawyers make in this area"],
  "recent_developments": "Any recent legal developments (note: knowledge has a cutoff date)",
  "cross_references": ["Related legal topic 1", "Related legal topic 2"],
  "hi_answer": "Hindi answer summary (always include)",
  "mr_answer": "Marathi answer summary (always include)"
}}

Area of law: {area or "General Indian law"}
Query: {query}
{f"Context documents:{chr(10)}{truncate_for_api(context_docs, 3000)}" if context_docs else ""}"""
    return call_claude_json(prompt, max_tokens=2000, system=INDIAN_LAW_SYSTEM)
