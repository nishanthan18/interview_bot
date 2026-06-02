# utils/ui.py
from __future__ import annotations

import streamlit as st


def render_brand_header(title: str, subtitle: str | None = None, badge: str | None = None) -> None:
    badge_html = f'<div class="small-muted">{badge}</div>' if badge else ""
    subtitle_html = f'<div class="hero-sub">{subtitle}</div>' if subtitle else ""

    st.markdown(
        f"""
        <div class="hero-wrap">
            {badge_html}
            <div class="hero-title">{title}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, caption: str | None = None) -> None:
    st.markdown(f"### {title}")
    if caption:
        st.caption(caption)


def render_metric_cards(metrics: list[dict]) -> None:
    cols = st.columns(len(metrics))
    for col, item in zip(cols, metrics):
        with col:
            label = item.get("label", "")
            value = item.get("value", "")
            delta = item.get("delta", None)
            col.metric(label, value, delta)


def render_feature_grid(items: list[dict], columns: int = 3) -> None:
    if not items:
        return

    for start in range(0, len(items), columns):
        row = items[start:start + columns]
        cols = st.columns(columns)
        for col, item in zip(cols, row):
            with col:
                st.markdown(
                    f"""
                    <div class="feature-tile">
                        <h4>{item.get('title', '')}</h4>
                        <p>{item.get('description', '')}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_info_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="glass-card">
            <h4>{title}</h4>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(title: str, text: str, action_label: str | None = None, action_key: str | None = None) -> bool:
    st.markdown(
        f"""
        <div class="glass-card" style="text-align:center; padding:2rem;">
            <h3>{title}</h3>
            <p class="small-muted">{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if action_label:
        return st.button(action_label, key=action_key or action_label, use_container_width=True)
    return False


def render_chat_history(messages: list[dict]) -> None:
    for msg in messages:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        with st.chat_message("assistant" if role == "assistant" else "user"):
            st.markdown(content)


def render_two_column_cards(left_title: str, left_body: str, right_title: str, right_body: str) -> None:
    c1, c2 = st.columns(2)
    with c1:
        render_info_card(left_title, left_body)
    with c2:
        render_info_card(right_title, right_body)


def render_status_pill(text: str, color: str = "#8ab4ff") -> None:
    st.markdown(
        f"""
        <span style="
            display:inline-block;
            padding:6px 12px;
            border-radius:999px;
            background:rgba(138,180,255,0.12);
            border:1px solid rgba(138,180,255,0.35);
            color:{color};
            font-size:0.88rem;
            font-weight:600;
            margin-bottom:8px;
        ">{text}</span>
        """,
        unsafe_allow_html=True,
    )


def render_page_tip(text: str) -> None:
    st.info(text)


def render_authenticated_sidebar(user: dict) -> None:
    with st.sidebar:
        st.markdown("## Interview Prep")
        st.caption(user.get("email", "Signed in"))

        if user.get("avatar_url"):
            st.image(user["avatar_url"], width=64)

        st.markdown("---")
        st.markdown("### Quick actions")
        st.page_link("app.py", label="Dashboard", icon="🏠")
        st.page_link("app.py", label="Practice", icon="💬")
        st.page_link("app.py", label="Mock Interview", icon="🎤")
        st.page_link("app.py", label="Progress", icon="📈")


def render_top_actions(labels: list[str], key_prefix: str = "top_action") -> str | None:
    cols = st.columns(len(labels))
    clicked = None
    for i, label in enumerate(labels):
        with cols[i]:
            if st.button(label, key=f"{key_prefix}_{i}", use_container_width=True):
                clicked = label
    return clicked


def render_history_selector(
    sessions: list[dict],
    label: str = "Recent sessions",
    key: str = "history_selector",
    format_func=None
):
    if not sessions:
        st.caption("No saved sessions yet.")
        return None

    def default_formatter(item: dict) -> str:
        title = item.get("title", "Untitled")
        created = item.get("created_at", "")
        return f"{title} · {created[:10]}"

    formatter = format_func or default_formatter
    return st.selectbox(label, sessions, format_func=formatter, key=key)


def render_upload_block(title: str, accepted_types: list[str]):
    st.markdown(f"### {title}")
    return st.file_uploader("Choose a file", type=accepted_types)


def render_result_block(title: str, content: str) -> None:
    st.markdown(f"### {title}")
    st.markdown(
        f"""
        <div class="glass-card">
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )