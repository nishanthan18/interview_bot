import streamlit as st


def goto(page_name: str):
    st.query_params["page"] = page_name


_GOOGLE_SVG = """
<svg width="18" height="18" viewBox="0 0 18 18" fill="none"
     xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0;">
  <path fill="#4285F4"
        d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844
           a4.14 4.14 0 0 1-1.796 2.716v2.259h2.908
           c1.702-1.567 2.684-3.875 2.684-6.615Z"/>
  <path fill="#34A853"
        d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259
           c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711
           H.957v2.332A8.997 8.997 0 0 0 9 18Z"/>
  <path fill="#FBBC05"
        d="M3.964 10.71A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.71
           V4.958H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.042
           l3.007-2.332Z"/>
  <path fill="#EA4335"
        d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58
           C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.958
           L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58Z"/>
</svg>
"""


def google_login_button(text: str = "Continue with Google", key: str = "google_login_btn"):
    st.markdown("<div class='google-login-shell'>", unsafe_allow_html=True)

    st.markdown(f"""
        <div class="google-login-visual">
            {_GOOGLE_SVG}
            <span>{text}</span>
        </div>
    """, unsafe_allow_html=True)

    clicked = st.button(text, use_container_width=True, key=key)

    st.markdown("</div>", unsafe_allow_html=True)

    if clicked:
        st.info("Google sign-in is not configured yet in deployment.")


def render_public_topbar():
    page = st.query_params.get("page", "landing")
    _, login_col, signup_col = st.columns([6, 1.15, 1.15])

    with login_col:
        if page != "login":
            if st.button("Login", use_container_width=True, key="topbar_login"):
                goto("login")

    with signup_col:
        if page != "signup":
            if st.button("Sign Up", use_container_width=True, type="primary", key="topbar_signup"):
                goto("signup")


def logout_user():
    for key in ["app_logged_in", "app_user"]:
        if key in st.session_state:
            del st.session_state[key]
    goto("landing")
    st.rerun()