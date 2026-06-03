import streamlit as st


def render_dashboard(user):
    name = user.get("full_name") or user.get("email", "User")
    first_name = name.split()[0] if name else "User"

    st.markdown("""
    <style>
    /* ── Dashboard layout ── */
    .dash-header {
        margin-bottom: 2rem;
    }
    .dash-greeting {
        font-size: 0.82rem;
        font-weight: 500;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #6366f1;
        margin-bottom: 4px;
    }
    .dash-title {
        font-size: 2rem;
        font-weight: 700;
        color: #f1f5f9;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .dash-subtitle {
        font-size: 0.88rem;
        color: #64748b;
        margin-top: 4px;
    }

    /* ── Metric cards ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 24px;
    }
    .kpi-card {
        background: #0f1117;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 20px 22px;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        border-radius: 14px 14px 0 0;
    }
    .kpi-card.blue::before  { background: #6366f1; }
    .kpi-card.teal::before  { background: #14b8a6; }
    .kpi-card.green::before { background: #22c55e; }
    .kpi-card.amber::before { background: #f59e0b; }

    .kpi-icon {
        font-size: 1.3rem;
        margin-bottom: 10px;
    }
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        color: #475569;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #f1f5f9;
        letter-spacing: -1px;
        line-height: 1;
        margin-bottom: 6px;
    }
    .kpi-sub {
        font-size: 0.76rem;
        color: #475569;
        line-height: 1.5;
    }

    /* ── Section cards ── */
    .s-card {
        background: #0f1117;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 22px 24px;
        margin-bottom: 16px;
        height: 100%;
    }
    .s-card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 14px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .s-card-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
        flex-shrink: 0;
    }
    .s-card-icon.purple { background: rgba(99,102,241,0.15); }
    .s-card-icon.teal   { background: rgba(20,184,166,0.15); }
    .s-card-icon.green  { background: rgba(34,197,94,0.15); }
    .s-card-icon.amber  { background: rgba(245,158,11,0.15); }

    .s-card-title {
        font-size: 0.88rem;
        font-weight: 600;
        color: #e2e8f0;
        letter-spacing: 0.01em;
    }
    .s-card-body {
        font-size: 0.83rem;
        color: #64748b;
        line-height: 1.7;
    }

    /* ── Focus pill ── */
    .focus-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99,102,241,0.12);
        border: 1px solid rgba(99,102,241,0.25);
        color: #818cf8;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 20px;
        padding: 4px 12px;
        margin-bottom: 12px;
    }

    /* ── Step list ── */
    .step-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 9px 0;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        font-size: 0.82rem;
        color: #94a3b8;
    }
    .step-item:last-child { border-bottom: none; }
    .step-num {
        width: 22px;
        height: 22px;
        border-radius: 6px;
        background: rgba(99,102,241,0.15);
        color: #818cf8;
        font-size: 0.7rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        margin-top: 1px;
    }

    /* ── Streak bar ── */
    .streak-row {
        display: flex;
        gap: 5px;
        margin-top: 10px;
    }
    .streak-day {
        flex: 1;
        height: 28px;
        border-radius: 5px;
        background: rgba(99,102,241,0.12);
        border: 1px solid rgba(99,102,241,0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.62rem;
        color: #475569;
        font-weight: 600;
    }
    .streak-day.active {
        background: rgba(99,102,241,0.35);
        border-color: rgba(99,102,241,0.55);
        color: #a5b4fc;
    }
    .streak-day.today {
        background: #6366f1;
        border-color: #6366f1;
        color: #fff;
    }

    /* ── Profile badge ── */
    .profile-badge {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 14px 0 16px 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 14px;
    }
    .profile-avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        font-weight: 700;
        color: white;
        flex-shrink: 0;
    }
    .profile-name {
        font-size: 0.9rem;
        font-weight: 600;
        color: #e2e8f0;
    }
    .profile-email {
        font-size: 0.75rem;
        color: #475569;
        margin-top: 2px;
    }
    .profile-badge-pill {
        margin-left: auto;
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.25);
        color: #4ade80;
        font-size: 0.7rem;
        font-weight: 600;
        border-radius: 20px;
        padding: 3px 10px;
    }

    /* ── Readiness ring (CSS only) ── */
    .ring-wrap {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-top: 8px;
    }
    .ring-svg { flex-shrink: 0; }
    .ring-info-label {
        font-size: 0.75rem;
        color: #475569;
        margin-bottom: 2px;
    }
    .ring-info-val {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f1f5f9;
        letter-spacing: -0.5px;
    }
    .ring-info-sub {
        font-size: 0.72rem;
        color: #475569;
        margin-top: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Header ──
    initials = "".join(p[0].upper() for p in name.split()[:2]) if name else "U"
    email = user.get("email", "")

    st.markdown(f"""
    <div class="dash-header">
        <div class="dash-greeting">Good day</div>
        <div class="dash-title">Welcome back, {first_name} 👋</div>
        <div class="dash-subtitle">Here's your interview prep overview for today.</div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ──
    st.markdown("""
    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="kpi-icon">📚</div>
            <div class="kpi-label">Practice Sessions</div>
            <div class="kpi-value">18</div>
            <div class="kpi-sub">Across technical &amp; HR modules</div>
        </div>
        <div class="kpi-card teal">
            <div class="kpi-icon">🎤</div>
            <div class="kpi-label">Mock Interviews</div>
            <div class="kpi-value">6</div>
            <div class="kpi-sub">Structured with evaluation flow</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-icon">🎯</div>
            <div class="kpi-label">Readiness Score</div>
            <div class="kpi-value">82%</div>
            <div class="kpi-sub">Based on consistency &amp; coverage</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-icon">🚀</div>
            <div class="kpi-label">Target Role</div>
            <div class="kpi-value" style="font-size:1.4rem;">SDE</div>
            <div class="kpi-sub">Track your selected path</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Main content ──
    left, right = st.columns([1.5, 1], gap="medium")

    with left:
        # Today's focus
        st.markdown("""
        <div class="s-card">
            <div class="s-card-header">
                <div class="s-card-icon purple">🧠</div>
                <div class="s-card-title">Today's Preparation Focus</div>
            </div>
            <div class="focus-pill">⚡ Daily Plan Active</div>
            <div class="s-card-body">
                Continue with <strong style="color:#c7d2fe;">DSA fundamentals</strong> and
                <strong style="color:#c7d2fe;">frontend interview questions</strong>, complete one
                <strong style="color:#c7d2fe;">HR round practice</strong>, and review one
                <strong style="color:#c7d2fe;">mock interview</strong> for stronger confidence.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Next steps
        st.markdown("""
        <div class="s-card">
            <div class="s-card-header">
                <div class="s-card-icon green">✅</div>
                <div class="s-card-title">Recommended Next Steps</div>
            </div>
            <ul class="step-list">
                <li class="step-item">
                    <span class="step-num">1</span>
                    Practice role-based questions in the Practice module.
                </li>
                <li class="step-item">
                    <span class="step-num">2</span>
                    Complete one full mock interview session.
                </li>
                <li class="step-item">
                    <span class="step-num">3</span>
                    Improve your resume summary using the Resume tool.
                </li>
                <li class="step-item">
                    <span class="step-num">4</span>
                    Review salary and company insights before applying.
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with right:
        # Profile card
        st.markdown(f"""
        <div class="s-card">
            <div class="s-card-header">
                <div class="s-card-icon teal">👤</div>
                <div class="s-card-title">Profile</div>
            </div>
            <div class="profile-badge">
                <div class="profile-avatar">{initials}</div>
                <div>
                    <div class="profile-name">{name}</div>
                    <div class="profile-email">{email}</div>
                </div>
                <div class="profile-badge-pill">Active</div>
            </div>
            <div class="s-card-body">
                Signed in via Google. Your workspace is ready for personalised
                interview preparation workflows.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Weekly streak
        st.markdown("""
        <div class="s-card">
            <div class="s-card-header">
                <div class="s-card-icon amber">🔥</div>
                <div class="s-card-title">Weekly Streak</div>
            </div>
            <div class="s-card-body">
                You're building consistency. Keep daily practice active to
                improve recall, fluency, and confidence.
            </div>
            <div class="streak-row">
                <div class="streak-day active">M</div>
                <div class="streak-day active">T</div>
                <div class="streak-day active">W</div>
                <div class="streak-day active">T</div>
                <div class="streak-day today">F</div>
                <div class="streak-day">S</div>
                <div class="streak-day">S</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Readiness ring
        st.markdown("""
        <div class="s-card">
            <div class="s-card-header">
                <div class="s-card-icon purple">📊</div>
                <div class="s-card-title">Readiness Breakdown</div>
            </div>
            <div class="ring-wrap">
                <svg class="ring-svg" width="72" height="72" viewBox="0 0 72 72">
                    <circle cx="36" cy="36" r="28" fill="none"
                            stroke="rgba(99,102,241,0.12)" stroke-width="8"/>
                    <circle cx="36" cy="36" r="28" fill="none"
                            stroke="#6366f1" stroke-width="8"
                            stroke-dasharray="175.9" stroke-dashoffset="31.7"
                            stroke-linecap="round"
                            transform="rotate(-90 36 36)"/>
                    <text x="36" y="40" text-anchor="middle"
                          font-size="13" font-weight="700" fill="#f1f5f9">82%</text>
                </svg>
                <div>
                    <div class="ring-info-label">Overall Score</div>
                    <div class="ring-info-val">82 / 100</div>
                    <div class="ring-info-sub">Top 24% of learners</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)