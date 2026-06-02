import streamlit as st
from utils.db import create_chat_session, save_chat_message, get_chat_messages, list_sessions, save_interview_report
from utils.groq_helper import chat_completion

INTERVIEW_TYPES = ["Technical", "HR", "Mixed"]

MOCK_SYSTEM_PROMPT = """
You are an expert interviewer conducting a mock interview.
Ask one interview question at a time.
After each answer, briefly evaluate it and ask the next question.
When the user asks for feedback or summary, provide strengths, weaknesses,
score out of 10, and improvement tips.
"""

def render_mock_interview(user):
    user_id = user.get("id")

    st.title("Mock Interview")
    st.caption("Run a realistic multi-round mock interview with saved chat history.")

    interview_type = st.selectbox("Interview type", INTERVIEW_TYPES)

    sessions = list_sessions(user_id, "mock_interview") if user_id else []
    session_map = {"New session": None}
    for session in sessions:
        title = session.get("title", "Untitled Session")
        created = session.get("created_at", "")[:10]
        session_map[f"{title} · {created}"] = session["id"]

    selected_session_label = st.selectbox("Choose session", list(session_map.keys()))
    session_id = session_map[selected_session_label]

    if session_id:
        messages = get_chat_messages(session_id)
        for msg in messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    col1, col2 = st.columns([2, 1])
    with col1:
        user_input = st.chat_input("Answer the mock question or ask to start / end interview")
    with col2:
        save_report = st.button("Generate Report", use_container_width=True)

    if user_input and user_id:
        if not session_id:
            new_session = create_chat_session(
                user_id=user_id,
                title=f"{interview_type} Mock Interview",
                module_name="mock_interview"
            )
            if not new_session:
                st.error("Could not create session.")
                st.stop()
            session_id = new_session["id"]

        save_chat_message(session_id, user_id, "user", user_input, {"interview_type": interview_type})

        reply = chat_completion(
            MOCK_SYSTEM_PROMPT,
            [{"role": "user", "content": f"Interview type: {interview_type}\nUser input: {user_input}"}],
            temperature=0.5
        )

        save_chat_message(session_id, user_id, "assistant", reply, {"interview_type": interview_type})
        st.rerun()

    if save_report and session_id and user_id:
        messages = get_chat_messages(session_id)
        transcript = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

        report = chat_completion(
            "Analyze this mock interview transcript. Return score out of 10, strengths, weaknesses, and suggestions in clear bullet style.",
            [{"role": "user", "content": transcript}],
            temperature=0.3
        )

        save_interview_report({
            "user_id": user_id,
            "session_id": session_id,
            "interview_type": interview_type,
            "role_target": interview_type,
            "score": 8,
            "strengths": ["Communication"],
            "weaknesses": ["Needs deeper examples"],
            "suggestions": ["Use STAR method", "Add measurable outcomes"],
            "report_json": {"report_text": report},
        })

        st.success("Report generated and saved.")
        st.write(report)