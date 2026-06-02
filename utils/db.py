import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["anon_key"],
    )


@st.cache_resource
def get_supabase_admin() -> Client:
    return create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["service_role_key"],
    )


def _is_valid_value(value):
    if value is None:
        return False
    value = str(value).strip()
    return value != "" and value.lower() != "none"


def upsert_profile(user: dict):
    sb = get_supabase_admin()
    res = sb.table("profiles").upsert(user, on_conflict="id").execute()
    return res.data[0] if res.data else user


def create_chat_session(user_id: str, title: str, module_name: str):
    if not _is_valid_value(user_id):
        return None

    sb = get_supabase_admin()
    res = sb.table("chat_sessions").insert({
        "user_id": user_id,
        "title": title,
        "module_name": module_name,
    }).execute()
    return res.data[0] if res.data else None


def save_chat_message(session_id: str, user_id: str, role: str, content: str, metadata=None):
    if not _is_valid_value(session_id) or not _is_valid_value(user_id):
        return None

    sb = get_supabase_admin()
    res = sb.table("chat_messages").insert({
        "session_id": session_id,
        "user_id": user_id,
        "role": role,
        "content": content,
        "metadata": metadata or {},
    }).execute()
    return res.data[0] if res.data else None


def list_sessions(user_id: str, module_name: str | None = None):
    if not _is_valid_value(user_id):
        return []

    sb = get_supabase_admin()
    query = sb.table("chat_sessions").select("*").eq("user_id", user_id).order("created_at", desc=True)

    if module_name:
        query = query.eq("module_name", module_name)

    res = query.execute()
    return res.data or []


def get_chat_messages(session_id: str | None):
    if not _is_valid_value(session_id):
        return []

    sb = get_supabase_admin()
    res = (
        sb.table("chat_messages")
        .select("*")
        .eq("session_id", session_id)
        .order("created_at")
        .execute()
    )
    return res.data or []


def save_interview_report(payload: dict):
    sb = get_supabase_admin()
    res = sb.table("interview_reports").insert(payload).execute()
    return res.data[0] if res.data else None


def save_resume_review(payload: dict):
    sb = get_supabase_admin()
    res = sb.table("resume_reviews").insert(payload).execute()
    return res.data[0] if res.data else None


def save_study_plan(payload: dict):
    sb = get_supabase_admin()
    res = sb.table("study_plans").insert(payload).execute()
    return res.data[0] if res.data else None


def fetch_user_reports(user_id: str):
    if not _is_valid_value(user_id):
        return []

    sb = get_supabase_admin()
    res = (
        sb.table("interview_reports")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return res.data or []