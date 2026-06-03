import streamlit as st
from utils.auth import google_login_button, login_user


def render_login():
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    left, center, right = st.columns([1.1, 1, 1.1])

    with center:
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
            key="li_email"
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
            key="li_password"
        )

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

        if st.button("Sign In", type="primary", use_container_width=True, key="li_submit"):
            if not email.strip() or not password:
                st.markdown("""
                <div class="auth-error">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                         stroke="currentColor" stroke-width="2"
                         stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="8" x2="12" y2="12"/>
                        <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                    Please enter your email and password.
                </div>
                """, unsafe_allow_html=True)
            else:
                pending = st.session_state.get("pending_user", {})
                if pending.get("email") == email.strip() and pending.get("password") == password:
                    login_user({
                        "id": pending.get("email"),
                        "email": pending.get("email"),
                        "full_name": pending.get("username", "User"),
                        "avatar_url": "",
                        "auth_provider": "email",
                    })
                    st.success(f"Welcome back, **{pending['username']}**!")
                    st.rerun()
                else:
                    st.markdown("""
                    <div class="auth-error">
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                             stroke="currentColor" stroke-width="2"
                             stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="10"/>
                            <line x1="12" y1="8" x2="12" y2="12"/>
                            <line x1="12" y1="16" x2="12.01" y2="16"/>
                        </svg>
                        Invalid email or password. Please try again.
                    </div>
                    """, unsafe_allow_html=True)