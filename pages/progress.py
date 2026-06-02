import streamlit as st
import pandas as pd
from utils.db import fetch_user_reports

def render_progress(user):
    user_id = user.get("id")

    st.title("Progress Tracking")
    st.caption("Track saved interview reports and improvement trends.")

    reports = fetch_user_reports(user_id) if user_id else []

    if not reports:
        st.info("No reports found yet. Complete a mock interview first.")
        return

    df = pd.DataFrame(reports)
    st.dataframe(df[["interview_type", "role_target", "score", "created_at"]], use_container_width=True)

    if "score" in df.columns:
        chart_df = df.copy()
        chart_df["created_at"] = pd.to_datetime(chart_df["created_at"])
        chart_df = chart_df.sort_values("created_at")
        st.line_chart(chart_df.set_index("created_at")["score"])