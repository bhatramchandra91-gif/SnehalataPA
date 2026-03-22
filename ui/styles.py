CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tiro+Devanagari+Hindi&family=Crimson+Pro:wght@400;600&family=DM+Sans:wght@300;400;500&display=swap');
.stApp { background-color:#fdfcf9; }
.tricolour-strip { height:5px; background:linear-gradient(90deg,#FF9933 0%,#FF9933 33.3%,#ffffff 33.3%,#ffffff 66.6%,#138808 66.6%,#138808 100%); margin:-1rem -1rem 0; position:sticky; top:0; z-index:999; }
.nyay-title { font-family:'Crimson Pro',serif; font-size:2rem; font-weight:600; color:#0d2240; line-height:1.2; }
.nyay-title-hi { font-family:'Tiro Devanagari Hindi',serif; font-size:0.95rem; color:#7a6a52; margin-top:2px; }
.devanagari { font-family:'Tiro Devanagari Hindi',serif; line-height:1.9; }
.lang-badge { display:inline-block; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:500; margin-right:5px; }
.lang-en { background:#fff5ef; color:#d4500a; border:1px solid #f3c4a8; }
.lang-hi { background:#f0f4ff; color:#2d4baa; border:1px solid #b5c8f4; font-family:'Tiro Devanagari Hindi',serif; }
.lang-mr { background:#edf7ec; color:#138808; border:1px solid #9fd89a; font-family:'Tiro Devanagari Hindi',serif; }
.lang-mix { background:#f7f4ee; color:#7a6a52; border:1px solid #d9d3c5; }
.status-pass { background:#edf7ec; color:#138808; padding:3px 12px; border-radius:12px; font-size:0.8rem; font-weight:500; }
.status-warn { background:#fef8ec; color:#92600a; padding:3px 12px; border-radius:12px; font-size:0.8rem; font-weight:500; }
.status-fail { background:#fdf0ee; color:#c0392b; padding:3px 12px; border-radius:12px; font-size:0.8rem; font-weight:500; }
.issue-ok      { background:#edf7ec; border-left:3px solid #138808; padding:8px 12px; border-radius:0 6px 6px 0; margin:5px 0; font-size:0.88rem; line-height:1.6; }
.issue-warning { background:#fef8ec; border-left:3px solid #92600a; padding:8px 12px; border-radius:0 6px 6px 0; margin:5px 0; font-size:0.88rem; line-height:1.6; }
.issue-error   { background:#fdf0ee; border-left:3px solid #c0392b; padding:8px 12px; border-radius:0 6px 6px 0; margin:5px 0; font-size:0.88rem; line-height:1.6; }
.issue-info    { background:#eef3fb; border-left:3px solid #1a4b8c; padding:8px 12px; border-radius:0 6px 6px 0; margin:5px 0; font-size:0.88rem; line-height:1.6; }
.issue-hi      { font-family:'Tiro Devanagari Hindi',serif; font-size:0.77rem; color:#7a6a52; margin-top:3px; display:block; }
.overall-pass { background:#edf7ec; border:1px solid #9fd89a; border-radius:10px; padding:12px 18px; color:#0e4225; font-weight:500; margin-bottom:1rem; }
.overall-warn { background:#fef8ec; border:1px solid #f5c96e; border-radius:10px; padding:12px 18px; color:#5a3a06; font-weight:500; margin-bottom:1rem; }
.overall-fail { background:#fdf0ee; border:1px solid #f0a9a4; border-radius:10px; padding:12px 18px; color:#7a1a12; font-weight:500; margin-bottom:1rem; }
.result-card { background:white; border:1px solid rgba(26,18,8,0.09); border-radius:12px; padding:1.2rem 1.4rem; margin-bottom:1rem; box-shadow:0 2px 12px rgba(26,18,8,0.06); }
.result-card-title { font-family:'DM Sans',sans-serif; font-weight:500; font-size:1rem; color:#0d2240; }
.result-card-title-hi { font-family:'Tiro Devanagari Hindi',serif; font-size:0.75rem; color:#7a6a52; }
.deadline-row { display:flex; align-items:flex-start; gap:12px; padding:10px 12px; background:#fdfcf9; border:1px solid rgba(26,18,8,0.08); border-radius:8px; margin:5px 0; font-size:0.88rem; }
.deadline-date { font-family:'Crimson Pro',serif; font-weight:600; color:#0d2240; min-width:110px; font-size:0.95rem; }
.lang-detected-box { background:#f7f4ee; border:1px solid #d9d3c5; border-radius:8px; padding:8px 14px; font-size:0.84rem; color:#3d2f1a; margin:6px 0; }
[data-testid="stSidebar"] { background-color:#0d2240 !important; }
[data-testid="stSidebar"] * { color:rgba(255,255,255,0.85) !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 { color:white !important; }
.sidebar-section-title { color:rgba(255,165,0,0.75) !important; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; margin-top:0.8rem; }
.stSpinner > div { border-top-color:#d4500a !important; }
.stButton > button { background-color:#0d2240; color:white !important; border:none; border-radius:8px; font-family:'DM Sans',sans-serif; font-weight:500; padding:0.5rem 1.5rem; transition:background 0.2s; }
.stButton > button:hover { background-color:#1a3a5c !important; color:white !important; border:none; }
[data-testid="stFileUploader"] { border:2px dashed #d9d3c5; border-radius:10px; padding:0.8rem; background:#fdfcf9; }
</style>
"""
