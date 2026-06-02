import streamlit as st

def render_dashboard(user):
    st.title("Dashboard")
    st.caption(f"Welcome, {user.get('full_name') or user.get('email')}")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Practice Sessions</div>
            <div class="metric-value">18</div>
            <div class="metric-sub">Completed across technical and HR modules.</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Mock Interviews</div>
            <div class="metric-value">6</div>
            <div class="metric-sub">Structured sessions with evaluation flow.</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Readiness Score</div>
            <div class="metric-value">82%</div>
            <div class="metric-sub">Based on consistency and category coverage.</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Target Role</div>
            <div class="metric-value">SDE</div>
            <div class="metric-sub">Track progress for your selected path.</div>
        </div>
        """, unsafe_allow_html=True)

    left, right = st.columns([1.45, 1])

    with left:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Today’s preparation focus</div>
            <div class="section-sub">
                Continue with DSA fundamentals, frontend interview questions, one HR round practice,
                and one mock interview review for stronger confidence.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-card">
            <div class="section-title">Recommended next steps</div>
            <div class="section-sub">
                1. Practice role-based questions. <br>
                2. Complete one mock interview. <br>
                3. Improve your resume summary. <br>
                4. Review salary and company insights before applying.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Profile summary</div>
            <div class="section-sub">
                Signed in with Google. Your dashboard is ready for personalized interview preparation workflows.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-card">
            <div class="section-title">Weekly streak</div>
            <div class="section-sub">
                You are building consistency. Keep daily practice active to improve recall, fluency, and confidence.
            </div>
        </div>
        """, unsafe_allow_html=True)