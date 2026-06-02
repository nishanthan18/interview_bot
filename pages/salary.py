import streamlit as st
from utils.groq_helper import chat_completion

def render_salary(user):
    st.title("Salary Guidance")
    st.caption("Prepare salary expectations and negotiation responses.")

    role = st.text_input("Role", placeholder="e.g. Software Engineer")
    location = st.text_input("Location", placeholder="e.g. Chennai")
    experience = st.selectbox("Experience level", ["Fresher", "0-2 years", "2-5 years", "5+ years"])

    if st.button("Generate Salary Guidance", type="primary", use_container_width=True):
        prompt = f"""
        Give salary expectation guidance for role {role}, location {location}, experience {experience}.
        Include:
        1. expected range
        2. how to answer expected salary
        3. short negotiation script
        """

        result = chat_completion(
            "You are a salary negotiation coach.",
            [{"role": "user", "content": prompt}],
            temperature=0.4
        )

        st.subheader("Salary Guidance")
        st.write(result)