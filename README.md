# ⚖️ Nyay Prep — Indian Legal Assistant
### भारतीय विधिक सहायक · भारतीय कायदेशीर सहाय्यक

A complete AI-powered legal assistant for Indian lawyers built with Streamlit and Claude.
Supports **English, Hindi (हिंदी), Marathi (मराठी)** across all 12 tools.

---

## 🛠️ 12 Tools

| # | Tool | Hindi | What it does |
|---|------|-------|-------------|
| 1 | Document Drafting | दस्तावेज़ मसौदा | Draft plaints, petitions, affidavits, contracts |
| 2 | Legal Research | विधिक अनुसंधान | Research Indian case law and statutes |
| 3 | Contract Review | अनुबंध समीक्षा | Risk analysis, redlines, missing clauses |
| 4 | Client Communication | मुवक्किल संचार | Draft emails/WhatsApp in English/Hindi/Marathi |
| 5 | Due Diligence | उचित परिश्रम | Corporate, property, M&A due diligence |
| 6 | Discovery Support | खोज सहायता | Evidence analysis, timelines, interrogatories |
| 7 | Compliance Checks | अनुपालन जाँच | Check compliance with Indian laws |
| 8 | Billing & Admin | बिलिंग प्रशासन | Generate invoices with GST |
| 9 | Court Filing Prep | दाखिल तैयारी | Pre-filing checks, checklists, deadlines |
| 10 | Meeting Notes | बैठक नोट्स | Structure notes into action items & case notes |
| 11 | IP & Patent | बौद्धिक संपदा | Patent, trademark, copyright under Indian IP law |
| 12 | Knowledge Management | ज्ञान प्रबंधन | Query Indian law knowledge base |

---

## 📁 Folder Structure

```
nyay_prep/
│
├── app.py                          ← Entry point — run this
├── requirements.txt                ← Python dependencies
├── .env                            ← Local API key (create this, never commit)
├── .gitignore
│
├── .streamlit/
│   ├── config.toml                 ← Theme and server settings
│   └── secrets.toml.example        ← Template for Streamlit Cloud secrets
│
├── core/
│   ├── __init__.py
│   ├── claude_client.py            ← API client (works locally + cloud)
│   ├── tools.py                    ← All 12 tool analyzers
│   ├── language.py                 ← Hindi/Marathi/English detection
│   └── pdf_reader.py               ← PDF/DOCX text extraction
│
├── ui/
│   ├── __init__.py
│   ├── styles.py                   ← Custom CSS
│   ├── components.py               ← Shared UI components
│   └── results.py                  ← Court filing results renderer
│
├── pages/
│   ├── __init__.py
│   ├── p01_drafting.py             ← Document Drafting page
│   ├── p02_research.py             ← Legal Research page
│   └── p03_to_p12.py               ← All remaining 10 pages
│
├── data/
│   ├── __init__.py
│   └── courts.py                   ← Indian courts & document types
│
└── tests/
    ├── sample_english.txt           ← Test: English writ petition
    ├── sample_hindi.txt             ← Test: Hindi plaint
    └── sample_marathi.txt           ← Test: Marathi writ petition
```

---

## 🚀 Part 1: Run Locally in VS Code

### Step 1 — Open VS Code and create project
```bash
# Open terminal in VS Code (Ctrl + `)
mkdir nyay_prep
cd nyay_prep
# Unzip the downloaded files here
```

### Step 2 — Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

You'll see `(venv)` in your terminal — that means it's active.

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```
This takes 2-3 minutes. You'll see packages installing.

### Step 4 — Add your API key
Create a file called `.env` in the root `nyay_prep/` folder:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```
Get your API key from: https://console.anthropic.com

> **Important:** Never commit this file to GitHub. It's in `.gitignore` already.

### Step 5 — Run the app
```bash
streamlit run app.py
```
Your browser opens automatically at **http://localhost:8501**

### Stopping the app
Press `Ctrl + C` in the terminal.

---

## 🐙 Part 2: Upload to GitHub

### Step 1 — Install Git
Download from: https://git-scm.com/downloads
Verify: `git --version`

### Step 2 — Create GitHub account
Go to https://github.com and sign up (free).

### Step 3 — Create a new repository
1. Click the **+** button → **New repository**
2. Name it: `nyay-prep`
3. Set to **Public** (required for free Streamlit Cloud)
4. **Do NOT** check "Add README" (you already have one)
5. Click **Create repository**

### Step 4 — Push your code
Run these commands in your project folder:
```bash
git init
git add .
git commit -m "Initial commit — Nyay Prep v1"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/nyay-prep.git
git push -u origin main
```
Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 5 — Verify on GitHub
Go to `https://github.com/YOUR_USERNAME/nyay-prep`
You should see all your files there.

---

## ☁️ Part 3: Deploy on Streamlit Cloud (Free, No Code to Run)

Once on GitHub, anyone can use your app from a URL — no Python needed.

### Step 1 — Sign up for Streamlit Cloud
Go to **https://streamlit.io/cloud** → Sign in with GitHub

### Step 2 — Deploy the app
1. Click **"New app"**
2. Select your repository: `YOUR_USERNAME/nyay-prep`
3. Branch: `main`
4. Main file path: `app.py`
5. Click **"Deploy!"**

### Step 3 — Add your API key (IMPORTANT)
Your `.env` file was NOT uploaded (it's in `.gitignore`). Add the key in Streamlit Cloud:

1. In your deployed app dashboard, click **"⋮" (three dots)** → **Settings**
2. Click **"Secrets"** tab
3. Paste this:
```toml
ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
```
4. Click **Save**
5. The app restarts automatically

### Step 4 — Share your app
Your app is now live at:
```
https://YOUR_USERNAME-nyay-prep-app-XXXXX.streamlit.app
```
Share this URL with anyone — they can use it from any browser, no installation needed.

---

## 🔄 Updating Your App

Whenever you make changes locally:
```bash
git add .
git commit -m "describe your change"
git push
```
Streamlit Cloud automatically redeploys within ~1 minute.

---

## 🧪 Testing Step by Step

| Step | Tool | Test file / input |
|------|------|------------------|
| 1 | Court Filing Prep | Paste `tests/sample_english.txt` |
| 2 | Court Filing Prep | Paste `tests/sample_hindi.txt` — enable Hindi translations |
| 3 | Court Filing Prep | Paste `tests/sample_marathi.txt` — enable Marathi check |
| 4 | Document Drafting | Type "Draft bail application for client accused under IPC 420" |
| 5 | Legal Research | Ask "What is limitation for cheque bounce under Section 138?" |
| 6 | Contract Review | Paste any NDA or service agreement text |
| 7 | Client Communication | Type hearing outcome notes, select Hindi output |
| 8 | Meeting Notes | Type rough notes from a client meeting |
| 9 | Billing & Admin | Enter a matter description and time entries |
| 10 | Knowledge Mgmt | Ask "What are mandatory clauses in a commercial lease?" |

---

## ❓ Troubleshooting

**`ModuleNotFoundError`** → Run `pip install -r requirements.txt` again

**`ANTHROPIC_API_KEY not found`** → Check your `.env` file exists and has the correct key

**PDF extraction fails** → Make sure `PyMuPDF` is installed: `pip install PyMuPDF`

**Streamlit Cloud shows error** → Check Secrets are saved correctly (Settings → Secrets)

**App runs slowly** → Normal for the first request — Claude API takes 3-8 seconds

---

## 📞 Support
For API issues: https://console.anthropic.com
For Streamlit issues: https://docs.streamlit.io
