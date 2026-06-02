import streamlit as st
from utils.db import create_chat_session, save_chat_message, get_chat_messages, list_sessions
from utils.groq_helper import chat_completion

HR_TOPICS = [
    "Self Introduction",
    "Strengths and Weaknesses",
    "Leadership",
    "Teamwork",
    "Conflict Resolution",
    "Career Goals",
    "Time Management",
    "Pressure Handling",
    "Why Should We Hire You",
    "Behavioral Questions",
]

EXPERIENCE_LEVELS = ["Fresher", "Intern", "Entry Level", "Experienced"]

HR_SYSTEM_PROMPT = """
You are an expert HR interview coach.

Your responsibilities:
- Ask realistic HR interview questions.
- Evaluate the candidate's answer.
- Give:
  1. communication feedback
  2. clarity feedback
  3. confidence impression
  4. better answer using STAR if applicable
  5. one follow-up question

Be concise, clear, and professional.
"""

def render_hr_round(user):
    user_id = user.get("id")

    st.title("HR Interview Preparation")
    st.caption("Advanced HR interview coaching with realistic questions and structured answer improvement.")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.selectbox("Choose HR topic", HR_TOPICS)
    with col2:
        level = st.selectbox("Candidate type", EXPERIENCE_LEVELS)

    sessions = list_sessions(user_id, "hr_round") if user_id else []
    session_map = {"New session": None}

    for session in sessions:
        title = session.get("title", "Untitled Session")
        created = session.get("created_at", "")[:10]
        session_map[f"{title} · {created}"] = session["id"]

    selected_session_label = st.selectbox("Choose session", list(session_map.keys()))
    session_id = session_map[selected_session_label]

    history = []
    if session_id:
        history = get_chat_messages(session_id)
        for msg in history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    row = st.columns(4)
    if row[0].button("Ask HR Question", use_container_width=True):
        st.session_state["hr_prompt"] = f"Ask me one HR question on {topic} for a {level} candidate."
    if row[1].button("Behavioral Round", use_container_width=True):
        st.session_state["hr_prompt"] = f"Ask me a behavioral question on {topic} and evaluate my answer using STAR."
    if row[2].button("Tell Me About Yourself", use_container_width=True):
        st.session_state["hr_prompt"] = "Help me prepare a strong Tell me about yourself answer."
    if row[3].button("Improve My Answer", use_container_width=True):
        st.session_state["hr_prompt"] = f"Ask me to answer an HR question about {topic}, then improve my answer."

    user_input = st.chat_input("Write your HR answer or request a realistic HR question")

    if not user_input:
        user_input = st.session_state.pop("hr_prompt", None)

    if user_input and user_id:
        if not session_id:
            new_session = create_chat_session(
                user_id=user_id,
                title=f"{topic} HR Round",
                module_name="hr_round"
            )
            if not new_session:
                st.error("Could not create session.")
                st.stop()
            session_id = new_session["id"]
            history = []

        save_chat_message(session_id, user_id, "user", user_input, {
            "topic": topic,
            "level": level
        })

        with st.chat_message("user"):
            st.write(user_input)

        context_message = f"HR Topic: {topic}\nCandidate Type: {level}\nUser input: {user_input}"

        reply = chat_completion(
            HR_SYSTEM_PROMPT,
            history=history,
            latest_user_message=context_message,
            temperature=0.5
        )

        save_chat_message(session_id, user_id, "assistant", reply, {
            "topic": topic,
            "level": level
        })

        with st.chat_message("assistant"):
            st.write(reply)

        st.rerun()