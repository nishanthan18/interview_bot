import streamlit as st

def build_plan(role, level, topic):
    topic_text = topic if topic.strip() else "core interview fundamentals"
    return f"""
### Practice Plan
- Role: {role}
- Level: {level}
- Focus: {topic_text}

### Session Structure
1. Revise fundamentals related to {topic_text}.
2. Practice 10 interview questions for {role}.
3. Solve 2 scenario-based questions.
4. Summarize your answers in short bullet points.
5. Review weak areas and retry incorrect answers.
"""

def render_practice(user):
    st.title("Practice")

    if "practice_plan_message" not in st.session_state:
        st.session_state.practice_plan_message = ""

    if "practice_plan_content" not in st.session_state:
        st.session_state.practice_plan_content = ""

    col1, col2 = st.columns(2)

    with col1:
        role = st.selectbox(
            "Target role",
            ["Frontend Developer", "Backend Developer", "Full Stack Developer", "Data Analyst", "AI Engineer"],
            key="practice_role"
        )

    with col2:
        level = st.selectbox(
            "Difficulty",
            ["Beginner", "Intermediate", "Advanced"],
            key="practice_level"
        )

    topic = st.text_input(
        "Focus topic",
        placeholder="React hooks, DBMS, Python OOP, REST API...",
        key="practice_topic"
    )

    if st.button("Generate Practice Plan", type="primary", use_container_width=True, key="generate_practice_plan"):
        st.session_state.practice_plan_message = f"Practice plan ready for {role} - {level}"
        st.session_state.practice_plan_content = build_plan(role, level, topic)

    if st.session_state.practice_plan_message:
        st.success(st.session_state.practice_plan_message)

    if st.session_state.practice_plan_content:
        st.markdown(st.session_state.practice_plan_content)

    st.markdown("""
    <div class="section-card">
        <div class="section-title">Practice guidance</div>
        <div class="section-sub">
            Select a role, set your difficulty, choose a topic, and use this page as your structured interview preparation workspace.
        </div>
    </div>
    """, unsafe_allow_html=True)