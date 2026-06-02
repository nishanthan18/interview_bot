import streamlit as st
from utils.auth import google_login_button, goto


def render_login():
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    left, center, right = st.columns([1.1, 1, 1.1])

    with center:
        if "login_error" not in st.session_state:
            st.session_state.login_error = ""

        st.markdown("""
        <div class="auth-card">
            <div class="auth-badge">Welcome Back</div>
            <div class="auth-title">Sign in to your account</div>
            <div class="auth-subtitle">
                Continue your interview preparation journey
                right where you left off.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.get("signup_success"):
            st.success(st.session_state.signup_success)
            del st.session_state["signup_success"]

        google_login_button("Continue with Google", key="login_google")

        st.markdown("""
        <div class="auth-divider">or sign in with email</div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='auth-form'>", unsafe_allow_html=True)

        st.markdown("""
        <div class="field-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4
                         c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
            </svg>
            Email address
        </div>
        """, unsafe_allow_html=True)
        email = st.text_input(
            "Email address",
            placeholder="you@example.com",
            label_visibility="collapsed",
            key="li_email",
        )

        st.markdown("""
        <div class="field-label-row">
            <div class="field-label" style="margin-bottom:0;">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" stroke-width="2" stroke-linecap="round"
                     stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
                Password
            </div>
            <span class="field-label-link">Forgot password?</span>
        </div>
        """, unsafe_allow_html=True)
        password = st.text_input(
            "Password",
            placeholder="Enter your password",
            type="password",
            label_visibility="collapsed",
            key="li_password",
        )

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

        if st.button("Sign In", type="primary", use_container_width=True, key="li_submit"):
            st.session_state.login_error = ""

            if not email.strip() or not password:
                st.session_state.login_error = "Please enter your email and password."
            else:
                pending = st.session_state.get("pending_user", {})
                if pending.get("email") == email.strip() and pending.get("password") == password:
                    st.session_state["app_logged_in"] = True
                    st.session_state["app_user"] = {
                        "username": pending.get("username", ""),
                        "email": pending.get("email", ""),
                        "full_name": pending.get("username", ""),
                    }
                    st.session_state.selected_page = "Dashboard"
                    goto("dashboard")
                    st.rerun()
                else:
                    st.session_state.login_error = "Invalid email or password. Please try again."

        if st.session_state.login_error:
            st.markdown(f"""
            <div class="auth-error">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" stroke-width="2"
                     stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
                {st.session_state.login_error}
            </div>
            """, unsafe_allow_html=True)

        st.markdown(
            "<div class='auth-footer-text'>Don't have an account yet?</div>",
            unsafe_allow_html=True,
        )

        if st.button("Create a free account", use_container_width=True, key="login_to_signup"):
            goto("signup")