import streamlit as st
from utils.auth import goto


def render_landing():
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

    left, center, right = st.columns([1.2, 2.4, 1.2], vertical_alignment="center")

    with center:
        st.markdown("""
        <div class="hero-wrap">
            <div class="hero-card">
                <div class="hero-badge">AI Career Preparation Platform</div>
                <div class="hero-title">
                    Prepare smarter.<br>Interview with confidence.
                </div>
                <div class="hero-subtitle">
                    Your personal workspace for mock interviews, resume review,
                    study plans, company research, and progress tracking —
                    all powered by AI, all in one place.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

        b1, b2, b3 = st.columns([1, 1.4, 1])

        with b2:
            if st.button("Get Started Free", type="primary",
                         use_container_width=True, key="landing_cta"):
                goto("signup")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            st.markdown("""
                <div style="text-align:center; font-size:0.80rem; color:#94a3b8;">
                    Already have an account?&nbsp;
                    <span style="color:#4f6ef7; cursor:pointer; font-weight:600;"
                          onclick="window.location.href='?page=login'">
                        Sign in
                    </span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="text-align:center; font-size:0.78rem; color:#94a3b8;
                        letter-spacing:0.03em;">
                Free to use &nbsp;·&nbsp; Google sign-in &nbsp;·&nbsp; No credit card needed
            </div>
        """, unsafe_allow_html=True)