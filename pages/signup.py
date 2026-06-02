import re
import streamlit as st
from utils.auth import google_login_button, goto


def _valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


def render_signup():
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    left, center, right = st.columns([1.1, 1, 1.1])

    with center:
        if "signup_errors" not in st.session_state:
            st.session_state.signup_errors = []

        st.markdown("""
        <div class="auth-card">
            <div class="auth-badge">New Account</div>
            <div class="auth-title">Create your free account</div>
            <div class="auth-subtitle">
                Set up your personal interview prep workspace.
                No credit card required.
            </div>
        </div>
        """, unsafe_allow_html=True)

        google_login_button("Sign up with Google", key="signup_google")

        st.markdown("""
        <div class="auth-divider">or create with email</div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='auth-form'>", unsafe_allow_html=True)

        st.markdown("""
        <div class="field-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
            </svg>
            Username
        </div>
        """, unsafe_allow_html=True)
        username = st.text_input(
            "Username",
            placeholder="e.g. john_doe",
            label_visibility="collapsed",
            key="su_username",
        )

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
            key="su_email",
        )

        st.markdown("""
        <div class="field-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            Password
        </div>
        """, unsafe_allow_html=True)
        password = st.text_input(
            "Password",
            placeholder="Minimum 8 characters",
            type="password",
            label_visibility="collapsed",
            key="su_password",
        )

        st.markdown("""
        <div class="field-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
            Confirm password
        </div>
        """, unsafe_allow_html=True)
        confirm = st.text_input(
            "Confirm password",
            placeholder="Re-enter your password",
            type="password",
            label_visibility="collapsed",
            key="su_confirm",
        )

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

        if st.button("Create Account", type="primary", use_container_width=True, key="su_submit"):
            errors = []

            if not username.strip():
                errors.append("Username is required.")
            elif len(username.strip()) < 3:
                errors.append("Username must be at least 3 characters.")

            if not email.strip():
                errors.append("Email address is required.")
            elif not _valid_email(email.strip()):
                errors.append("Please enter a valid email address.")

            if not password:
                errors.append("Password is required.")
            elif len(password) < 8:
                errors.append("Password must be at least 8 characters.")

            if password and confirm != password:
                errors.append("Passwords do not match.")

            st.session_state.signup_errors = errors

            if not errors:
                st.session_state["pending_user"] = {
                    "username": username.strip(),
                    "email": email.strip(),
                    "password": password,
                }
                st.session_state["signup_success"] = (
                    f"Account created for {username.strip()} successfully. Please sign in."
                )
                goto("login")
                st.rerun()

        if st.session_state.signup_errors:
            for e in st.session_state.signup_errors:
                st.markdown(f"""
                <div class="auth-error">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                         stroke="currentColor" stroke-width="2"
                         stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="8" x2="12" y2="12"/>
                        <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                    {e}
                </div>
                """, unsafe_allow_html=True)

        st.markdown(
            "<div class='auth-footer-text'>Already have an account?</div>",
            unsafe_allow_html=True,
        )

        if st.button("Sign in instead", use_container_width=True, key="signup_to_login"):
            goto("login")