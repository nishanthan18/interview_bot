import re
import io
import streamlit as st
from utils.db import save_resume_review
from utils.groq_helper import chat_completion

# ── optional parsers (graceful fallback) ──────────────────────────────────────
try:
    import pdfplumber
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    from docx import Document as DocxDocument
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False

# ── keyword library ───────────────────────────────────────────────────────────
COMMON_KEYWORDS = {
    "python developer": [
        "python", "flask", "django", "fastapi", "sql", "mysql", "postgresql",
        "rest api", "git", "github", "oop", "debugging", "javascript",
        "html", "css", "react", "testing", "deployment", "docker", "linux"
    ],
    "frontend developer": [
        "html", "css", "javascript", "react", "redux", "typescript",
        "responsive design", "api integration", "git", "ui", "ux",
        "debugging", "webpack", "figma", "accessibility"
    ],
    "data analyst": [
        "python", "sql", "excel", "power bi", "tableau", "pandas",
        "data cleaning", "visualization", "statistics", "reporting",
        "numpy", "matplotlib", "machine learning"
    ],
    "backend developer": [
        "node.js", "express", "python", "java", "spring", "rest api",
        "graphql", "sql", "mongodb", "redis", "docker", "kubernetes",
        "ci/cd", "microservices", "linux"
    ],
    "data scientist": [
        "python", "machine learning", "deep learning", "tensorflow", "pytorch",
        "scikit-learn", "pandas", "numpy", "statistics", "nlp",
        "sql", "feature engineering", "model deployment", "a/b testing"
    ],
    "devops engineer": [
        "docker", "kubernetes", "ci/cd", "jenkins", "github actions",
        "terraform", "ansible", "linux", "aws", "azure", "gcp",
        "monitoring", "bash", "python", "networking"
    ],
}

EXPERIENCE_LEVELS = ["Fresher", "Intern", "0-2 years", "2-5 years", "5+ years"]

# ── CSS ───────────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* ── header ── */
.rv-header {
    display: flex; align-items: center; gap: 14px;
    padding: 26px 0 10px;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 26px;
}
.rv-header-icon {
    width: 44px; height: 44px; background: #111827;
    border-radius: 11px; display: flex; align-items: center; justify-content: center;
}
.rv-header h1 {
    font-family: 'Syne', sans-serif; font-size: 1.5rem;
    font-weight: 700; color: #0f172a; margin: 0; letter-spacing: -0.4px;
}
.rv-header p { font-size: 0.82rem; color: #64748b; margin: 3px 0 0; }

/* ── section label ── */
.sec-label {
    font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; color: #94a3b8; margin: 22px 0 8px;
    display: flex; align-items: center; gap: 7px;
}

/* ── upload zone ── */
.upload-hint {
    font-size: 0.78rem; color: #94a3b8; margin-top: 5px;
}

/* ── score cards ── */
.score-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 14px; margin: 18px 0;
}
.score-card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 18px 20px;
    position: relative; overflow: hidden;
}
.score-card::before {
    content: ''; position: absolute; top: 0; left: 0;
    width: 4px; height: 100%; background: var(--accent);
    border-radius: 4px 0 0 4px;
}
.score-card.green  { --accent: #16a34a; }
.score-card.amber  { --accent: #d97706; }
.score-card.red    { --accent: #dc2626; }
.score-card.blue   { --accent: #2563eb; }
.score-card-label  { font-size: 0.71rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.7px; color: #94a3b8; }
.score-card-value  { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 700; color: #0f172a; margin: 4px 0 0; line-height: 1; }
.score-card-sub    { font-size: 0.75rem; color: #64748b; margin-top: 5px; }

/* ── gauge bar ── */
.gauge-wrap { margin: 6px 0 0; }
.gauge-track {
    height: 5px; background: #f1f5f9; border-radius: 99px; overflow: hidden;
}
.gauge-fill {
    height: 100%; border-radius: 99px;
    background: var(--accent); transition: width 0.6s ease;
}

/* ── keyword pills ── */
.pill-wrap { display: flex; flex-wrap: wrap; gap: 7px; margin: 8px 0 14px; }
.pill {
    display: inline-block; padding: 4px 11px;
    border-radius: 20px; font-size: 0.75rem; font-weight: 500;
}
.pill-match  { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
.pill-miss   { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }

/* ── issue row ── */
.issue-row {
    display: flex; align-items: flex-start; gap: 10px;
    background: #fffbeb; border: 1px solid #fde68a;
    border-radius: 8px; padding: 11px 14px; margin-bottom: 8px;
    font-size: 0.83rem; color: #78350f; line-height: 1.5;
}
.ok-row {
    display: flex; align-items: center; gap: 10px;
    background: #f0fdf4; border: 1px solid #bbf7d0;
    border-radius: 8px; padding: 11px 14px;
    font-size: 0.83rem; color: #15803d;
}

/* ── verdict card ── */
.verdict-card {
    border-radius: 12px; padding: 20px 22px; margin-top: 8px;
    display: flex; align-items: flex-start; gap: 14px;
}
.verdict-good   { background: #f0fdf4; border: 1px solid #86efac; }
.verdict-mid    { background: #fffbeb; border: 1px solid #fde68a; }
.verdict-low    { background: #fef2f2; border: 1px solid #fca5a5; }
.verdict-title  { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.05rem; margin-bottom: 4px; }
.verdict-body   { font-size: 0.83rem; line-height: 1.55; color: #475569; }

/* ── review prose ── */
.review-wrap {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 22px 24px; margin-top: 4px;
    font-size: 0.86rem; line-height: 1.7; color: #1e293b;
}

/* ── divider ── */
hr.rv-div { border: none; border-top: 1px solid #e2e8f0; margin: 22px 0; }

/* ── Streamlit overrides ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stFileUploader"] label {
    font-size: 0.73rem !important; font-weight: 700 !important;
    color: #475569 !important; text-transform: uppercase; letter-spacing: 0.6px;
}
.stButton > button {
    font-family: 'DM Sans', sans-serif; font-size: 0.85rem;
    font-weight: 600; border-radius: 9px;
    padding: 11px 18px; transition: all 0.15s;
}
div[data-testid="stMetric"] { display: none; }
</style>
"""

# ── inline SVG helpers ─────────────────────────────────────────────────────────
def icon(d, size=15, color="currentColor", stroke=2):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke}" '
            f'stroke-linecap="round" stroke-linejoin="round">{d}</svg>')

IC_FILE     = icon('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>')
IC_SCAN     = icon('<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><line x1="7" y1="12" x2="17" y2="12"/>')
IC_TAG      = icon('<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>')
IC_WARN     = icon('<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>', color="#d97706")
IC_CHECK    = icon('<polyline points="20 6 9 17 4 12"/>', color="#16a34a")
IC_X        = icon('<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>', color="#dc2626")
IC_REPORT   = icon('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>')
IC_SETTINGS = icon('<circle cx="12" cy="12" r="3"/><path d="M19.07 4.93A10 10 0 1 0 21 12"/>')
IC_UPLOAD   = icon('<polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/>')
IC_STAR     = icon('<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>')

# ── text extraction ───────────────────────────────────────────────────────────
def extract_text_from_file(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    raw = uploaded_file.read()

    if name.endswith(".pdf"):
        if not PDF_SUPPORT:
            st.error("pdfplumber not installed. Run: pip install pdfplumber")
            return ""
        with pdfplumber.open(io.BytesIO(raw)) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages]
        return "\n".join(pages)

    if name.endswith(".docx"):
        if not DOCX_SUPPORT:
            st.error("python-docx not installed. Run: pip install python-docx")
            return ""
        doc = DocxDocument(io.BytesIO(raw))
        return "\n".join(p.text for p in doc.paragraphs)

    if name.endswith(".txt"):
        return raw.decode("utf-8", errors="replace")

    st.warning("Unsupported file type. Please upload PDF, DOCX, or TXT.")
    return ""

# ── analysis helpers ──────────────────────────────────────────────────────────
def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def extract_keywords(text: str):
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+.#/-]{1,}", text.lower())
    stopwords = {
        "the","and","with","for","you","your","are","from","that","this",
        "have","will","our","job","role","all","but","not","into","using",
        "use","about","can","has","had","was","were","their","them","they",
        "his","her","she","him","its","who","why","how","what","when"
    }
    filtered = [w for w in words if w not in stopwords and len(w) > 2]
    freq = {}
    for w in filtered:
        freq[w] = freq.get(w, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:30]]


def ats_format_score(resume_text: str):
    score = 100
    issues = []
    lower  = resume_text.lower()

    standard_sections = ["summary", "education", "skills", "experience", "projects"]
    found = [s for s in standard_sections if s in lower]
    if len(found) < 3:
        score -= 20
        missing_sec = [s for s in standard_sections if s not in found]
        issues.append(f"Missing standard sections: {', '.join(s.upper() for s in missing_sec)}. ATS parsers rely on these headings.")

    if "|" in resume_text or "\t" in resume_text:
        score -= 10
        issues.append("Column-like separators or tab characters detected. ATS tools may mis-parse multi-column layouts.")

    if len(resume_text.split()) < 150:
        score -= 10
        issues.append("Resume is too brief (under 150 words). Add more detail so ATS has sufficient text to evaluate.")

    if re.search(r"[^\x00-\x7F]", resume_text):
        score -= 5
        issues.append("Non-ASCII or special characters detected. Replace them with standard equivalents for full ATS compatibility.")

    if "objective" in lower and "summary" not in lower:
        score -= 5
        issues.append("Outdated OBJECTIVE section found. Replace with a professional SUMMARY for modern ATS and recruiter expectations.")

    if not re.search(r"\b\d{4}\b", resume_text):
        score -= 5
        issues.append("No years detected. Add employment dates (e.g. 2022 – 2024) so ATS can assess experience duration.")

    bullets = resume_text.count("•") + resume_text.count("-") + resume_text.count("*")
    if bullets < 5:
        score -= 5
        issues.append("Very few bullet points detected. Use bullets to list achievements and responsibilities for better ATS parsing.")

    return max(score, 0), issues


def keyword_match_score(resume_text: str, jd_text: str, target_role: str):
    resume_lower = normalize_text(resume_text)
    keywords = extract_keywords(jd_text) if jd_text.strip() else COMMON_KEYWORDS.get(target_role.lower(), [])
    if not keywords:
        return 0, [], []
    matched = [kw for kw in keywords if kw in resume_lower]
    missing = [kw for kw in keywords if kw not in resume_lower]
    score   = int((len(matched) / len(keywords)) * 100)
    return score, matched, missing


def section_depth_score(resume_text: str):
    """Score how well each major section is developed."""
    lower  = resume_text.lower()
    result = {}
    checks = {
        "Contact Info":   bool(re.search(r"[\w.+-]+@[\w-]+\.\w+", resume_text)),
        "Summary":        "summary" in lower or "profile" in lower,
        "Skills":         "skills" in lower,
        "Experience":     "experience" in lower or "work history" in lower,
        "Education":      "education" in lower or "degree" in lower or "university" in lower,
        "Projects":       "project" in lower,
        "Certifications": "certif" in lower or "certification" in lower,
        "Quantified Results": bool(re.search(r"\d+\s*%|\$\d+|\d+\s*(users|clients|teams|projects)", lower)),
    }
    for label, present in checks.items():
        result[label] = present
    score = int((sum(checks.values()) / len(checks)) * 100)
    return score, result


def generate_resume_review(resume_text, jd_text, target_role, experience, missing_keywords):
    prompt = f"""
You are an expert ATS resume reviewer and hiring coach.

Target Role: {target_role}
Experience Level: {experience}

Job Description:
{jd_text if jd_text.strip() else "Not provided — use general best practices for the target role."}

Resume:
{resume_text}

Missing Keywords: {', '.join(missing_keywords) if missing_keywords else "None identified"}

Provide a structured, professional review covering:
1. ATS Suitability Summary
2. Role Suitability Summary
3. What to Update (specific, actionable)
4. Missing or Weak Sections
5. Top 5 Keyword Additions with usage examples
6. 3 Improved Bullet-Point Examples (rewrite weak bullets with quantification)
7. Improved Professional Summary (rewritten)
8. Final Verdict: Is this resume ready to apply?
"""
    return chat_completion(
        "You are a precise ATS resume optimization expert. Be direct, specific, and actionable.",
        history=[],
        latest_user_message=prompt,
        temperature=0.3,
    )

# ── score card HTML ───────────────────────────────────────────────────────────
def score_card(label, value, sub, color_class):
    pct = min(value, 100)
    return f"""
<div class="score-card {color_class}">
    <div class="score-card-label">{label}</div>
    <div class="score-card-value">{value}<span style="font-size:1rem;color:#94a3b8">/100</span></div>
    <div class="gauge-wrap">
        <div class="gauge-track"><div class="gauge-fill" style="width:{pct}%"></div></div>
    </div>
    <div class="score-card-sub">{sub}</div>
</div>"""

def color_for(score):
    if score >= 80: return "green"
    if score >= 60: return "amber"
    return "red"

# ── main render ───────────────────────────────────────────────────────────────
def render_resume(user):
    user_id = user.get("id")

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # ── header ─────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="rv-header">
        <div class="rv-header-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
                 fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
            </svg>
        </div>
        <div>
            <h1>Resume ATS Checker</h1>
            <p>Upload or paste your resume &mdash; get ATS scores, keyword analysis, and an AI-powered improvement report</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── configuration ───────────────────────────────────────────────────────────
    st.markdown(f'<div class="sec-label">{IC_SETTINGS}&nbsp; Configuration</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        target_role = st.text_input("Target Role", placeholder="e.g. Python Developer")
    with col2:
        experience = st.selectbox("Experience Level", EXPERIENCE_LEVELS)

    # ── resume input ────────────────────────────────────────────────────────────
    st.markdown(f'<div class="sec-label">{IC_UPLOAD}&nbsp; Resume Input</div>', unsafe_allow_html=True)

    input_mode = st.radio(
        "Input method",
        ["Upload File (PDF / DOCX / TXT)", "Paste Text"],
        horizontal=True,
        label_visibility="collapsed",
    )

    resume_text = ""
    uploaded_filename = "pasted_resume.txt"

    if input_mode == "Upload File (PDF / DOCX / TXT)":
        uploaded = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx", "txt"],
            label_visibility="collapsed",
        )
        st.markdown('<p class="upload-hint">Supported formats: PDF, DOCX, TXT &mdash; max 5 MB</p>', unsafe_allow_html=True)
        if uploaded:
            with st.spinner("Extracting text from file…"):
                resume_text = extract_text_from_file(uploaded)
            uploaded_filename = uploaded.name
            if resume_text:
                with st.expander("Extracted Text Preview", expanded=False):
                    st.text(resume_text[:1200] + ("…" if len(resume_text) > 1200 else ""))
    else:
        resume_text = st.text_area(
            "Paste Resume Text",
            height=300,
            placeholder="Paste your full resume content here…",
            label_visibility="collapsed",
        )

    # ── job description ──────────────────────────────────────────────────────────
    st.markdown(f'<div class="sec-label">{IC_TAG}&nbsp; Job Description (optional but recommended)</div>', unsafe_allow_html=True)
    jd_text = st.text_area(
        "Job Description",
        height=180,
        placeholder="Paste the job posting here to enable precise keyword matching…",
        label_visibility="collapsed",
    )

    st.markdown('<hr class="rv-div">', unsafe_allow_html=True)

    # ── analyse button ───────────────────────────────────────────────────────────
    run = st.button("Analyse Resume", type="primary", use_container_width=True)

    if run:
        if not resume_text.strip():
            st.warning("Please upload or paste your resume before analysing.")
            st.stop()

        with st.spinner("Running ATS analysis…"):
            ats_score,   ats_issues             = ats_format_score(resume_text)
            match_score, matched_kws, missing_kws = keyword_match_score(resume_text, jd_text, target_role)
            depth_score, depth_map              = section_depth_score(resume_text)

        final_score = int((ats_score * 0.35) + (match_score * 0.40) + (depth_score * 0.25))

        # ── scores ──────────────────────────────────────────────────────────────
        st.markdown(f'<div class="sec-label">{IC_STAR}&nbsp; Score Overview</div>', unsafe_allow_html=True)

        cards_html = '<div class="score-grid">'
        cards_html += score_card("ATS Format",    ats_score,   "Formatting & structure compliance", color_for(ats_score))
        cards_html += score_card("Keyword Match", match_score, "Overlap with role / JD keywords",   color_for(match_score))
        cards_html += score_card("Section Depth", depth_score, "Completeness of resume sections",   color_for(depth_score))
        cards_html += '</div>'
        cards_html += f'<div class="score-grid">'
        cards_html += score_card("Overall Fit", final_score,
                                 "Weighted composite (35% ATS + 40% keywords + 25% depth)",
                                 "blue")
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

        # ── ATS issues ──────────────────────────────────────────────────────────
        st.markdown('<hr class="rv-div">', unsafe_allow_html=True)
        st.markdown(f'<div class="sec-label">{IC_SCAN}&nbsp; ATS Format Issues</div>', unsafe_allow_html=True)

        if ats_issues:
            for issue in ats_issues:
                st.markdown(f'<div class="issue-row">{IC_WARN}&nbsp;{issue}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ok-row">{IC_CHECK}&nbsp;No major ATS formatting issues detected.</div>', unsafe_allow_html=True)

        # ── section depth ───────────────────────────────────────────────────────
        st.markdown('<hr class="rv-div">', unsafe_allow_html=True)
        st.markdown(f'<div class="sec-label">{IC_FILE}&nbsp; Section Completeness</div>', unsafe_allow_html=True)

        depth_cols = st.columns(4)
        for i, (section, present) in enumerate(depth_map.items()):
            col = depth_cols[i % 4]
            tick    = IC_CHECK if present else IC_X
            bg      = "#f0fdf4" if present else "#fef2f2"
            border  = "#bbf7d0" if present else "#fecaca"
            txt_col = "#15803d" if present else "#b91c1c"
            col.markdown(
                f'<div style="background:{bg};border:1px solid {border};border-radius:8px;'
                f'padding:10px 12px;font-size:0.78rem;font-weight:600;color:{txt_col};'
                f'display:flex;align-items:center;gap:7px;margin-bottom:8px;">'
                f'{tick}&nbsp;{section}</div>',
                unsafe_allow_html=True,
            )

        # ── keyword analysis ────────────────────────────────────────────────────
        st.markdown('<hr class="rv-div">', unsafe_allow_html=True)
        st.markdown(f'<div class="sec-label">{IC_TAG}&nbsp; Keyword Analysis</div>', unsafe_allow_html=True)

        kw_col1, kw_col2 = st.columns(2)
        with kw_col1:
            st.markdown('<div style="font-size:0.78rem;font-weight:600;color:#15803d;margin-bottom:6px;">Matched Keywords</div>', unsafe_allow_html=True)
            if matched_kws:
                pills = "".join(f'<span class="pill pill-match">{k}</span>' for k in matched_kws[:20])
                st.markdown(f'<div class="pill-wrap">{pills}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="font-size:0.82rem;color:#94a3b8;">No strong matches found.</p>', unsafe_allow_html=True)

        with kw_col2:
            st.markdown('<div style="font-size:0.78rem;font-weight:600;color:#b91c1c;margin-bottom:6px;">Missing Keywords</div>', unsafe_allow_html=True)
            if missing_kws:
                pills = "".join(f'<span class="pill pill-miss">{k}</span>' for k in missing_kws[:20])
                st.markdown(f'<div class="pill-wrap">{pills}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="font-size:0.82rem;color:#94a3b8;">No significant gaps detected.</p>', unsafe_allow_html=True)

        # ── AI review ────────────────────────────────────────────────────────────
        st.markdown('<hr class="rv-div">', unsafe_allow_html=True)
        st.markdown(f'<div class="sec-label">{IC_REPORT}&nbsp; AI-Powered Review</div>', unsafe_allow_html=True)

        with st.spinner("Generating detailed AI review…"):
            review = generate_resume_review(
                resume_text=resume_text,
                jd_text=jd_text,
                target_role=target_role or "the stated role",
                experience=experience,
                missing_keywords=missing_kws[:15],
            )

        st.markdown(f'<div class="review-wrap">{review}</div>', unsafe_allow_html=True)

        # ── verdict ──────────────────────────────────────────────────────────────
        st.markdown('<hr class="rv-div">', unsafe_allow_html=True)
        st.markdown(f'<div class="sec-label">{IC_STAR}&nbsp; Final Verdict</div>', unsafe_allow_html=True)

        if final_score >= 80:
            v_class  = "verdict-good"
            v_icon   = IC_CHECK
            v_title  = "Strong ATS Fit — Ready to Apply"
            v_body   = "Your resume scores well across formatting, keyword coverage, and section depth. Minor refinements may still improve your edge but you are in a strong position to submit."
        elif final_score >= 60:
            v_class  = "verdict-mid"
            v_icon   = IC_WARN
            v_title  = "Moderate Fit — Updates Recommended"
            v_body   = "Your resume has a reasonable foundation but gaps in keywords or section depth may cause ATS filtering before a recruiter sees it. Address the flagged issues before applying."
        else:
            v_class  = "verdict-low"
            v_icon   = IC_X
            v_title  = "Low Fit — Resume Needs Significant Work"
            v_body   = "Your resume is likely to be filtered out by ATS before reaching a recruiter. Review the issues above carefully and rebuild weak sections before submitting applications."

        st.markdown(f"""
        <div class="verdict-card {v_class}">
            <div style="flex-shrink:0;margin-top:2px;">{v_icon}</div>
            <div>
                <div class="verdict-title">{v_title}</div>
                <div class="verdict-body">{v_body}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── save ─────────────────────────────────────────────────────────────────
        if user_id:
            save_resume_review({
                "user_id":   user_id,
                "filename":  uploaded_filename,
                "ats_score": final_score,
                "keyword_gaps": missing_kws[:20],
                "section_scores": {
                    "ats_format_score":  ats_score,
                    "keyword_match_score": match_score,
                    "section_depth_score": depth_score,
                    "matched_keywords":  matched_kws[:20],
                    "section_depth_map": depth_map,
                    "review_text":       review,
                    "verdict":           v_title,
                },
            })
            st.markdown(
                f'<div class="ok-row" style="margin-top:14px;">{IC_CHECK}&nbsp;'
                f'Review saved to your profile.</div>',
                unsafe_allow_html=True,
            )