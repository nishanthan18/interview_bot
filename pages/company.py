import streamlit as st
from utils.groq_helper import chat_completion

def render_company(user):
    st.title("Company Preparation")
    st.caption("Prepare company-specific interview questions, answers, and smart questions to ask.")

    company_name = st.text_input("Company name", placeholder="e.g. TCS, Infosys, Zoho")
    role_name = st.text_input("Target role", placeholder="e.g. Python Developer")
    company_context = st.text_area("Paste company/job details (optional)", height=180)

    if st.button("Generate Company Prep", type="primary", use_container_width=True):
        if not company_name.strip():
            st.warning("Please enter a company name.")
            st.stop()

        prompt = f"""
Prepare interview guidance for this company.

Company: {company_name}
Role: {role_name}
Context: {company_context}

Return:
1. Company interview overview
2. What they may ask for this role
3. 10 likely interview questions
4. Tips to answer well
5. 5 smart questions to ask the interviewer
"""

        result = chat_completion(
            system_prompt="You are an expert interview coach who gives company-specific preparation advice.",
            history=[],
            latest_user_message=prompt,
            temperature=0.4
        )

        st.subheader("Preparation Guide")
        st.write(result)