import streamlit as st


def apply_global_styles(theme: str = "light"):
    is_dark = theme == "dark"

    # ── palette ──────────────────────────────────────────────────────────
    bg          = "#0f1117"   if is_dark else "#f8fafc"
    surface     = "#1a1d2e"   if is_dark else "#ffffff"
    surface2    = "#242840"   if is_dark else "#f1f5f9"
    sidebar     = "#13162a"   if is_dark else "#ffffff"
    border      = "#2a2e4a"   if is_dark else "#e2e8f0"
    text        = "#f0f2ff"   if is_dark else "#0f172a"
    sub         = "#8b93b8"   if is_dark else "#64748b"
    accent      = "#4f6ef7"
    accent_h    = "#3b5bef"
    danger      = "#ef4444"
    button_border = "#2e3356" if is_dark else "#e2e8f0"
    card_shadow = "0 4px 24px rgba(0,0,0,0.32)" if is_dark else "0 4px 24px rgba(15,23,42,0.08)"

    st.markdown(f"""
<style>
/* ── Google Font ──────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Reset & base ─────────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; }}

html, body, [data-testid="stAppViewContainer"] {{
    background: {bg} !important;
    font-family: 'DM Sans', sans-serif;
    color: {text};
}}

[data-testid="stHeader"] {{ display: none !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}
footer {{ display: none !important; }}
#MainMenu {{ display: none !important; }}

/* ── Main content area ────────────────────────── */
[data-testid="stMainBlockContainer"] {{
    padding-top: 0 !important;
    max-width: 100% !important;
}}

/* ── Sidebar ──────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: {sidebar} !important;
    border-right: 1px solid {border} !important;
}}
[data-testid="stSidebarNav"] {{ display: none !important; }}
div[data-testid="collapsedControl"] {{ display: none !important; }}

/* ── Sidebar brand ────────────────────────────── */
.sidebar-shell {{ padding: 6px 2px; }}

.sidebar-brand-clean {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 4px 20px 4px;
    margin-bottom: 4px;
    color: {text};
}}
.brand-mark {{
    width: 40px; height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, {accent}, {accent_h});
    display: flex; align-items: center; justify-content: center;
    color: white;
    box-shadow: 0 8px 20px rgba(79,110,247,0.30);
    flex-shrink: 0;
}}
.brand-title {{
    font-size: 0.95rem;
    font-weight: 700;
    color: {text};
    line-height: 1.2;
}}
.brand-subtitle {{
    font-size: 0.78rem;
    color: {sub};
    margin-top: 2px;
    font-weight: 400;
}}

/* ── User panel ───────────────────────────────── */
.user-panel {{
    background: {surface2};
    border: 1px solid {border};
    border-radius: 14px;
    padding: 14px 16px;
    margin: 0 0 14px 0;
}}
.user-panel-top {{
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {sub};
    font-weight: 600;
    margin-bottom: 4px;
}}
.user-panel-name {{
    font-size: 0.95rem;
    font-weight: 700;
    color: {text};
    line-height: 1.3;
}}
.user-panel-email {{
    font-size: 0.80rem;
    color: {sub};
    margin-top: 2px;
    word-break: break-all;
}}

/* ── Sidebar nav ──────────────────────────────── */
.sidebar-section-title {{
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: {sub};
    font-weight: 700;
    margin: 16px 0 6px 4px;
}}
.sidebar-divider {{
    height: 1px;
    background: {border};
    margin: 12px 0;
}}
.theme-switch-label {{
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: {sub};
    font-weight: 700;
    margin: 12px 0 6px 4px;
}}

[data-testid="stSidebar"] .stButton > button {{
    justify-content: flex-start;
    text-align: left;
    height: 42px;
    border-radius: 10px;
    border: 1px solid {button_border} !important;
    background: transparent !important;
    color: {text} !important;
    padding: 0 14px;
    font-weight: 500;
    font-size: 0.88rem;
    transition: background 0.15s, border-color 0.15s;
    font-family: 'DM Sans', sans-serif;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: rgba(79,110,247,0.09) !important;
    border-color: rgba(79,110,247,0.22) !important;
}}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, {accent}, {accent_h}) !important;
    color: #fff !important;
    border-color: transparent !important;
    font-weight: 600;
    box-shadow: 0 4px 14px rgba(79,110,247,0.28);
}}

/* ── Auth card (login / signup) ───────────────── */
.auth-wrap {{
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 82vh;
}}
.auth-card {{
    background: {surface};
    border: 1px solid {border};
    border-radius: 20px;
    padding: 36px 32px 28px 32px;
    box-shadow: {card_shadow};
    text-align: center;
    margin-bottom: 20px;
}}
.auth-badge {{
    display: inline-block;
    background: rgba(79,110,247,0.12);
    color: {accent};
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 50px;
    margin-bottom: 14px;
}}
.auth-title {{
    font-size: 1.55rem;
    font-weight: 800;
    color: {text};
    line-height: 1.2;
    margin-bottom: 10px;
    letter-spacing: -0.02em;
}}
.auth-subtitle {{
    font-size: 0.90rem;
    color: {sub};
    line-height: 1.6;
    max-width: 320px;
    margin: 0 auto 6px auto;
}}
.auth-divider {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 18px 0;
    color: {sub};
    font-size: 0.82rem;
}}
.auth-divider::before,
.auth-divider::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: {border};
}}
.auth-footer-text {{
    text-align: center;
    font-size: 0.84rem;
    color: {sub};
    margin: 14px 0 6px 0;
}}
.auth-info-box {{
    background: rgba(79,110,247,0.07);
    border: 1px solid rgba(79,110,247,0.18);
    border-radius: 12px;
    padding: 14px 16px;
    font-size: 0.84rem;
    color: {sub};
    line-height: 1.6;
    text-align: left;
    margin: 10px 0 6px 0;
}}
.auth-info-box strong {{
    color: {text};
    font-weight: 600;
}}
.auth-steps {{
    list-style: none;
    padding: 0;
    margin: 10px 0 0 0;
    text-align: left;
}}
.auth-steps li {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 0.84rem;
    color: {sub};
    margin-bottom: 8px;
    line-height: 1.5;
}}
.auth-steps li .step-num {{
    min-width: 22px; height: 22px;
    border-radius: 50%;
    background: rgba(79,110,247,0.14);
    color: {accent};
    font-size: 0.75rem;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}}
.auth-steps li .step-text strong {{
    color: {text};
    font-weight: 600;
}}

/* ── Global buttons ───────────────────────────── */
.stButton > button {{
    font-family: 'DM Sans', sans-serif;
    border-radius: 10px;
    height: 44px;
    font-weight: 600;
    font-size: 0.88rem;
    transition: all 0.15s;
}}
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, {accent}, {accent_h}) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(79,110,247,0.28);
}}
.stButton > button[kind="primary"]:hover {{
    box-shadow: 0 6px 20px rgba(79,110,247,0.40);
    transform: translateY(-1px);
}}
.stButton > button[kind="secondary"] {{
    background: {surface} !important;
    color: {text} !important;
    border: 1px solid {border} !important;
}}
.stButton > button[kind="secondary"]:hover {{
    border-color: {accent} !important;
    color: {accent} !important;
}}

/* ── Hero (landing) ───────────────────────────── */
.hero-wrap {{
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 0 24px 0;
}}
.hero-card {{
    text-align: center;
    max-width: 640px;
}}
.hero-badge {{
    display: inline-block;
    background: rgba(79,110,247,0.12);
    color: {accent};
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 50px;
    margin-bottom: 18px;
}}
.hero-title {{
    font-size: 2.6rem;
    font-weight: 800;
    color: {text};
    line-height: 1.18;
    letter-spacing: -0.03em;
    margin-bottom: 18px;
}}
.hero-subtitle {{
    font-size: 1.05rem;
    color: {sub};
    line-height: 1.7;
    max-width: 540px;
    margin: 0 auto;
}}

/* ── Topbar ───────────────────────────────────── */
.public-topbar {{
    border-bottom: 1px solid {border};
    padding: 14px 32px;
    display: flex;
    align-items: center;
    background: {bg};
    margin-bottom: 8px;
}}

/* ── Theme toggle icon buttons ────────────────── */
[data-testid="stSidebar"] button[key="theme_light"]::before,
[data-testid="stSidebar"] .stButton > button[data-testid="theme_light"]::before {{
    content: '';
}}

/* Use CSS mask to inject sun icon on Light button */
[data-testid="stSidebar"] [data-testid="column"]:first-child .stButton > button {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
}}
[data-testid="stSidebar"] [data-testid="column"]:last-child .stButton > button {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
}}

/* ── Google auth button ───────────────────────── */
/* The .google-btn-visual row shows the icon+label.
   The actual st.button is hidden beneath it via negative margin + opacity 0,
   so clicks still register on the real Streamlit button.          */
.google-btn-wrapper {{
    position: relative;
}}
.google-btn-visual {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    background: #fff;
    color: #1a1a2e;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    height: 48px;
    font-weight: 600;
    font-size: 0.92rem;
    font-family: 'DM Sans', sans-serif;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07);
    cursor: pointer;
    transition: box-shadow 0.15s, transform 0.15s;
    margin-bottom: -48px;   /* pull button up so it overlaps */
    position: relative;
    z-index: 2;
    pointer-events: none;   /* clicks pass through to button below */
}}
.google-btn-visual span {{
    line-height: 1;
}}
.google-btn-wrapper:hover .google-btn-visual {{
    box-shadow: 0 3px 12px rgba(0,0,0,0.13);
    transform: translateY(-1px);
}}
.google-btn-wrapper .stButton > button {{
    opacity: 0 !important;
    height: 48px !important;
    position: relative;
    z-index: 1;
}}

/* ── Auth form fields ─────────────────────────── */
.auth-form {{
    margin-top: 4px;
}}
.field-label {{
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.82rem;
    font-weight: 600;
    color: {text};
    margin: 12px 0 5px 2px;
    letter-spacing: 0.01em;
}}
.field-label-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 12px 0 5px 2px;
}}
.field-label-link {{
    font-size: 0.78rem;
    color: {accent};
    cursor: pointer;
    font-weight: 500;
}}
.field-label-link:hover {{
    text-decoration: underline;
}}

/* Style Streamlit text inputs inside auth pages */
[data-testid="stTextInput"] > div > div > input {{
    background: {surface2} !important;
    border: 1.5px solid {border} !important;
    border-radius: 10px !important;
    color: {text} !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 10px 14px !important;
    height: 44px !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}}
[data-testid="stTextInput"] > div > div > input:focus {{
    border-color: {accent} !important;
    box-shadow: 0 0 0 3px rgba(79,110,247,0.14) !important;
    outline: none !important;
}}
[data-testid="stTextInput"] > div > div > input::placeholder {{
    color: {sub} !important;
    opacity: 0.7 !important;
}}

/* ── Auth error message ───────────────────────── */
.auth-error {{
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.22);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.84rem;
    color: #ef4444;
    margin: 8px 0;
    font-weight: 500;
}}


/* ── Theme toggle visual track ────────────────── */
.theme-toggle-track {{
    display: flex;
    gap: 6px;
    background: {surface2};
    border: 1px solid {border};
    border-radius: 12px;
    padding: 4px;
    margin-bottom: 4px;
}}
.theme-pill {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    height: 32px;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
    pointer-events: none;
}}
.theme-pill-active {{
    background: {accent};
    color: #fff;
    box-shadow: 0 2px 8px rgba(79,110,247,0.30);
}}
.theme-pill-inactive {{
    color: {sub};
    background: transparent;
}}

/* ── Nav item visual (icon + label overlay) ───── */
.nav-item-visual {{
    display: flex;
    align-items: center;
    gap: 10px;
    height: 42px;
    padding: 0 14px;
    border-radius: 10px;
    font-size: 0.88rem;
    font-weight: 500;
    font-family: 'DM Sans', sans-serif;
    pointer-events: none;
    margin-bottom: -46px;
    position: relative;
    z-index: 2;
}}
.nav-item-active {{
    background: linear-gradient(135deg, {accent}, {accent_h});
    color: #fff;
    box-shadow: 0 4px 14px rgba(79,110,247,0.28);
    font-weight: 600;
}}
.nav-item-inactive {{
    color: {text};
    background: transparent;
}}

.nav-item-logout {{
    color: {sub};
    margin-top: 4px;
}}
.nav-item-logout:hover {{
    color: {danger};
}}
/* The underlying Streamlit button stays clickable but invisible */
[data-testid="stSidebar"] .stButton > button {{
    opacity: 0 !important;
    position: relative !important;
    z-index: 3 !important;
}}
/* Restore active/hover state visually through the .nav-item-visual instead */
/* Pull the hidden Streamlit theme buttons over the visual track */
[data-testid="stSidebar"] .theme-toggle-track + div [data-testid="column"]:nth-child(1) .stButton > button,
[data-testid="stSidebar"] .theme-toggle-track + div [data-testid="column"]:nth-child(2) .stButton > button {{
    opacity: 0 !important;
    height: 40px !important;
    margin-top: -44px !important;
    position: relative !important;
    z-index: 10 !important;
}}
</style>
""", unsafe_allow_html=True)