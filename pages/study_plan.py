import streamlit as st
from utils.db import save_study_plan
from utils.groq_helper import chat_completion

def render_study_plan(user):
    user_id = user.get("id")

    st.title("Study Plan")
    st.caption("Generate a week-by-week preparation roadmap.")

    role_target = st.text_input("Target role", placeholder="e.g. Frontend Developer")
    duration = st.slider("Duration in weeks", 1, 12, 4)
    current_level = st.selectbox("Current level", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate Study Plan", type="primary", use_container_width=True):
        prompt = f"""
        Create a {duration}-week study plan for a {current_level} candidate targeting {role_target}.
        Include weekly goals, topics, practice tasks, and interview prep.
        """

        plan = chat_completion(
            "You are an interview preparation planner.",
            [{"role": "user", "content": prompt}],
            temperature=0.4
        )

        st.subheader("Generated Plan")
        st.write(plan)

        if user_id:
            save_study_plan({
                "user_id": user_id,
                "role_target": role_target,
                "duration_weeks": duration,
                "plan_json": {"plan_text": plan},
            })