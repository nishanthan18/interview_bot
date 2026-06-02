import streamlit as st
from utils.styles import apply_global_styles
from utils.state import init_state
from utils.auth import render_public_topbar, logout_user

from pages.landing import render_landing
from pages.login import render_login
from pages.signup import render_signup
from pages.dashboard import render_dashboard
from pages.practice import render_practice
from pages.mock_interview import render_mock_interview
from pages.hr_round import render_hr_round
from pages.non_tech_roles import render_non_tech_roles
from pages.resume import render_resume
from pages.study_plan import render_study_plan
from pages.salary import render_salary
from pages.company import render_company
from pages.progress import render_progress


st.set_page_config(
    page_title="Interview Prep — AI Career Workspace",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def sync_logged_in_user():
    """Extract user profile from st.user after Google OAuth."""
    if not hasattr(st, "user") or not st.user.is_logged_in:
        return None

    def _read(attr_name):
        try:
            return getattr(st.user, attr_name, "") or ""
        except Exception:
            return ""

    return {
        "id":            str(_read("sub")),
        "email":         _read("email"),
        "full_name":     _read("name"),
        "avatar_url":    _read("picture"),
        "auth_provider": "google",
    }


# ── Init ──────────────────────────────────────────────────────────────────────
init_state()
apply_global_styles(st.session_state.get("theme", "light"))

page = st.query_params.get("page", "landing")

# ── Public routes (not logged in) ─────────────────────────────────────────────
if not hasattr(st, "user") or not st.user.is_logged_in:
    render_public_topbar()

    if page == "login":
        render_login()
    elif page == "signup":
        render_signup()
    else:
        render_landing()

    st.stop()

# ── Authenticated area ────────────────────────────────────────────────────────
user = sync_logged_in_user()
if user is None:
    st.error("Unable to load user profile. Please try logging in again.")
    if st.button("Back to Login"):
        st.query_params["page"] = "login"
        st.rerun()
    st.stop()

# ── Navigation config ─────────────────────────────────────────────────────────
# SVG icons (Feather-style) for each nav item — embedded as HTML labels
# Streamlit button labels are plain text, so we render icons above buttons
# using a separate HTML block that is purely decorative.
NAV_SECTIONS = {
    "Main": [
        "Dashboard",
        "Practice",
        "Mock Interview",
        "HR Round",
        "Progress",
    ],
    "Tools": [
        "Resume",
        "Study Plan",
        "Salary",
        "Company",
        "Non-Tech Roles",
    ],
}

NAV_ICONS = {
    "Dashboard":      '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
    "Practice":       '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>',
    "Mock Interview": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "HR Round":       '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "Progress":       '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6"  y1="20" x2="6"  y2="14"/></svg>',
    "Resume":         '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
    "Study Plan":     '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
    "Salary":         '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 1 0 0 7h5a3.5 3.5 0 1 1 0 7H6"/></svg>',
    "Company":        '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "Non-Tech Roles": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></svg>',
}

PAGE_RENDERERS = {
    "Dashboard":      render_dashboard,
    "Practice":       render_practice,
    "Mock Interview": render_mock_interview,
    "HR Round":       render_hr_round,
    "Non-Tech Roles": render_non_tech_roles,
    "Resume":         render_resume,
    "Study Plan":     render_study_plan,
    "Salary":         render_salary,
    "Company":        render_company,
    "Progress":       render_progress,
}

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Dashboard"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-shell'>", unsafe_allow_html=True)

    # Brand
    st.markdown("""
        <div class="sidebar-brand-clean">
            <div class="brand-mark">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                     aria-hidden="true">
                    <rect x="3"  y="3"  width="7" height="7" rx="2"
                          fill="currentColor"/>
                    <rect x="14" y="3"  width="7" height="7" rx="2"
                          fill="currentColor" opacity="0.72"/>
                    <rect x="3"  y="14" width="7" height="7" rx="2"
                          fill="currentColor" opacity="0.72"/>
                    <rect x="14" y="14" width="7" height="7" rx="2"
                          fill="currentColor"/>
                </svg>
            </div>
            <div>
                <div class="brand-title">Interview Prep</div>
                <div class="brand-subtitle">AI Career Workspace</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # User panel
    display_name  = user.get("full_name") or "Interview User"
    display_email = user.get("email", "")

    st.markdown(f"""
        <div class="user-panel">
            <div class="user-panel-top">Signed in</div>
            <div class="user-panel-name">{display_name}</div>
            <div class="user-panel-email">{display_email}</div>
        </div>
    """, unsafe_allow_html=True)

    # Theme toggle — rendered as custom HTML pill; Streamlit buttons are opacity:0 beneath
    is_light = st.session_state.get("theme", "light") == "light"
    st.markdown(f"""
        <div class="theme-switch-label">Appearance</div>
        <div class="theme-toggle-track">
            <div class="theme-pill {'theme-pill-active' if is_light else 'theme-pill-inactive'}">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" stroke-width="2.2"
                     stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="5"/>
                    <line x1="12" y1="1"  x2="12" y2="3"/>
                    <line x1="12" y1="21" x2="12" y2="23"/>
                    <line x1="4.22" y1="4.22"   x2="5.64" y2="5.64"/>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                    <line x1="1"  y1="12" x2="3"  y2="12"/>
                    <line x1="21" y1="12" x2="23" y2="12"/>
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
                </svg>
                Light
            </div>
            <div class="theme-pill {'theme-pill-inactive' if is_light else 'theme-pill-active'}">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" stroke-width="2.2"
                     stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                </svg>
                Dark
            </div>
        </div>
    """, unsafe_allow_html=True)

    t1, t2 = st.columns(2)
    with t1:
        if st.button("Light", use_container_width=True, key="theme_light"):
            st.session_state.theme = "light"
            st.rerun()

    with t2:
        if st.button("Dark", use_container_width=True, key="theme_dark"):
            st.session_state.theme = "dark"
            st.rerun()

    # Pull the real buttons up under the visual track
    st.markdown("<style>.theme-btn-offset { margin-top: -80px; }</style>",
                unsafe_allow_html=True)

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    # Nav links
    for section, items in NAV_SECTIONS.items():
        st.markdown(f"<div class='sidebar-section-title'>{section}</div>",
                    unsafe_allow_html=True)

        for item in items:
            active      = st.session_state.selected_page == item
            button_type = "primary" if active else "secondary"
            icon        = NAV_ICONS.get(item, "")

            # Render icon + label as an HTML overlay; the button below is the real target
            active_cls = "nav-item-active" if active else "nav-item-inactive"
            st.markdown(f"""
                <div class="nav-item-visual {active_cls}">
                    {icon}
                    <span>{item}</span>
                </div>
            """, unsafe_allow_html=True)

            if st.button(item, key=f"nav_{item}",
                         use_container_width=True, type=button_type):
                st.session_state.selected_page = item
                st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="nav-item-visual nav-item-logout">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                <polyline points="16 17 21 12 16 7"/>
                <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            <span>Logout</span>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Logout", use_container_width=True, key="sidebar_logout"):
        logout_user()

    st.markdown("</div>", unsafe_allow_html=True)

# ── Render selected page ───────────────────────────────────────────────────────
selected = st.session_state.selected_page
PAGE_RENDERERS[selected](user)