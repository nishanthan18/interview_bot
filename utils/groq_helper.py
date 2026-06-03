import streamlit as st
from groq import Groq


def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY") or st.secrets.get("groq", {}).get("api_key", "")
    return Groq(api_key=api_key)


def build_messages(system_prompt: str, history: list[dict], latest_user_message: str = None):
    messages = [{"role": "system", "content": system_prompt}]

    for item in history:
        role = item.get("role")
        content = item.get("content", "")
        if role in ["user", "assistant"] and content:
            messages.append({"role": role, "content": content})

    if latest_user_message:
        messages.append({"role": "user", "content": latest_user_message})

    return messages


def chat_completion(
    system_prompt: str,
    history: list[dict],
    latest_user_message: str = None,
    temperature: float = 0.4,
):
    try:
        client = get_groq_client()

        # Support both flat key and nested [groq] section
        try:
            model = st.secrets["groq"].get("model", "llama-3.3-70b-versatile")
        except Exception:
            model = st.secrets.get("GROQ_MODEL", "llama-3.3-70b-versatile")

        messages = build_messages(system_prompt, history, latest_user_message)

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )

        content = completion.choices[0].message.content
        return content.strip() if content else "I could not generate a response. Please try again."

    except Exception as e:
        return f"Error while contacting Groq API: {str(e)}"