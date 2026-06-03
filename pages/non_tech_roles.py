import streamlit as st
from utils.db import create_chat_session, save_chat_message, get_chat_messages, list_sessions
from utils.groq_helper import chat_completion

NON_TECH_ROLES = [
    "Business Analyst",
    "Customer Support",
    "Operations Executive",
    "Sales Associate",
    "HR Executive",
    "Product Intern",
    "Customer Success",
]

NON_TECH_SYSTEM_PROMPT = """
You are an expert interview coach for non-technical roles.

You help candidates prepare for analyst, operations, support, HR, sales, and customer-success roles.

For each response:
- ask a role-relevant interview question OR
- evaluate the candidate answer
- give strengths
- identify weak areas
- give an improved answer
- ask one realistic follow-up question

Keep the tone professional and concise.
"""

def render_non_tech_roles(user):
    user_id = user.get("id")

    st.title("Non-Tech Role Preparation")
    st.caption("Advanced preparation for analyst, support, operations, HR, sales, and customer-facing roles.")

    col1, col2 = st.columns(2)
    with col1:
        role_target = st.selectbox("Choose target role", NON_TECH_ROLES)
    with col2:
        focus = st.selectbox("Focus area", ["Interview Q&A", "Communication", "Scenario Handling", "Role Fit"])

    sessions = list_sessions(user_id, "non_tech_roles") if user_id else []
    session_map = {"New session": None}
    for session in sessions:
        title = session.get("title", "Untitled Session")
        created = session.get("created_at", "")[:10]
        session_map[f"{title} · {created}"] = session["id"]

    session_labels = list(session_map.keys())

    # Determine default index based on persisted session
    default_index = 0
    persisted_id = st.session_state.get("nontech_session_id")
    if persisted_id:
        for i, (label, sid) in enumerate(session_map.items()):
            if sid == persisted_id:
                default_index = i
                break

    selected_session_label = st.selectbox(
        "Choose session",
        session_labels,
        index=default_index,
        key="nontech_session_selector"
    )
    chosen_id = session_map[selected_session_label]

    # If user manually picks a different session from dropdown, update state
    if chosen_id != persisted_id:
        st.session_state["nontech_session_id"] = chosen_id
        persisted_id = chosen_id

    session_id = persisted_id

    # Load and display chat history
    history = []
    if session_id:
        history = get_chat_messages(session_id)
        for msg in history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # Quick-action buttons
    row = st.columns(4)
    if row[0].button("Ask Role Question", use_container_width=True):
        st.session_state["nontech_prompt"] = f"Ask me one interview question for a {role_target} role."
    if row[1].button("Situational Question", use_container_width=True):
        st.session_state["nontech_prompt"] = f"Ask me one situational question for {role_target} focused on {focus}."
    if row[2].button("Evaluate My Answer", use_container_width=True):
        st.session_state["nontech_prompt"] = f"Give me a {role_target} question and then evaluate my answer."
    if row[3].button("Role Fit Feedback", use_container_width=True):
        st.session_state["nontech_prompt"] = f"Tell me what interviewers expect from a strong {role_target} candidate."

    user_input = st.chat_input("Ask for a question, answer one, or request detailed role feedback")

    if not user_input:
        user_input = st.session_state.pop("nontech_prompt", None)

    if user_input and user_id:
        # Create a new session if none is active
        if not session_id:
            new_session = create_chat_session(
                user_id=user_id,
                title=f"{role_target} Prep",
                module_name="non_tech_roles"
            )
            if not new_session:
                st.error("Could not create session.")
                st.stop()
            session_id = new_session["id"]
            # Persist the new session so it survives rerun
            st.session_state["nontech_session_id"] = session_id
            history = []

        save_chat_message(session_id, user_id, "user", user_input, {
            "role_target": role_target,
            "focus": focus
        })

        with st.chat_message("user"):
            st.write(user_input)

        context_message = f"Target role: {role_target}\nFocus area: {focus}\nUser input: {user_input}"

        reply = chat_completion(
            NON_TECH_SYSTEM_PROMPT,
            history=history,
            latest_user_message=context_message,
            temperature=0.5
        )

        save_chat_message(session_id, user_id, "assistant", reply, {
            "role_target": role_target,
            "focus": focus
        })

        with st.chat_message("assistant"):
            st.write(reply)

        st.rerun()