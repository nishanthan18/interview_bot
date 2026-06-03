import base64
import json
import streamlit as st
from streamlit_oauth import OAuth2Component

try:
    GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
    GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
    APP_BASE_URL = st.secrets.get("APP_BASE_URL", "http://localhost:8501")
except Exception:
    GOOGLE_CLIENT_ID = ""
    GOOGLE_CLIENT_SECRET = ""
    APP_BASE_URL = "http://localhost:8501"

REDIRECT_URI = APP_BASE_URL.rstrip("/") + "/component/streamlit_oauth.oauth2"

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_URL = "https://oauth2.googleapis.com/revoke"


def goto(page_name: str):
    st.query_params["page"] = page_name


def login_user(user_data: dict):
    st.session_state.user = user_data
    st.session_state.app_user = user_data
    st.session_state.app_logged_in = True
    st.session_state.selected_page = "Dashboard"
    goto("dashboard")


def logout_user():
    for key in ["user", "app_user", "app_logged_in", "selected_page", "oauth_token"]:
        if key in st.session_state:
            del st.session_state[key]
    goto("landing")
    st.rerun()


def get_current_user():
    return st.session_state.get("app_user") or st.session_state.get("user")


def is_logged_in() -> bool:
    return bool(st.session_state.get("app_logged_in") or st.session_state.get("user"))


def require_login():
    if not is_logged_in():
        goto("login")
        st.rerun()


def _decode_jwt_payload(token: str) -> dict:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return {}
        payload = parts[1]
        payload += "=" * (-len(payload) % 4)
        decoded = base64.urlsafe_b64decode(payload.encode("utf-8"))
        return json.loads(decoded.decode("utf-8"))
    except Exception:
        return {}


def _oauth_client():
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        return None
    return OAuth2Component(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        authorize_endpoint=AUTHORIZE_URL,
        token_endpoint=TOKEN_URL,
        refresh_token_endpoint=TOKEN_URL,
        revoke_token_endpoint=REVOKE_URL,
    )


def google_login_button(text: str = "Continue with Google", key: str = "google_login_btn"):
    oauth2 = _oauth_client()

    if oauth2 is None:
        st.button(text, use_container_width=True, key=f"{key}_disabled", disabled=True)
        st.error(
            "Google OAuth is not configured. Add GOOGLE_CLIENT_ID, "
            "GOOGLE_CLIENT_SECRET and APP_BASE_URL in secrets.toml."
        )
        return

    result = oauth2.authorize_button(
        name=text,
        icon="https://www.google.com/favicon.ico",
        redirect_uri=REDIRECT_URI,
        scope="openid email profile",
        key=key,
        use_container_width=True,
        pkce="S256",
        extras_params={"prompt": "select_account", "access_type": "offline"},
    )

    if result and "token" in result:
        token_data = result["token"]
        id_token = token_data.get("id_token", "")
        payload = _decode_jwt_payload(id_token) if id_token else {}

        email = payload.get("email", "")
        full_name = payload.get("name", "")
        avatar_url = payload.get("picture", "")
        user_id = payload.get("sub", email)

        if not email:
            st.error("Google login failed: email was not returned in the ID token.")
            return

        user_data = {
            "id": user_id,
            "email": email,
            "full_name": full_name or email.split("@")[0],
            "avatar_url": avatar_url,
            "auth_provider": "google",
        }

        st.session_state.oauth_token = token_data
        login_user(user_data)
        st.rerun()


def render_public_topbar():
    # Brand-only navbar — no Login/Sign Up buttons here.
    # The landing page handles CTA ("Get Started Free" + "Sign in") directly.
    # The login/signup pages are reached via those CTAs.
    st.markdown("""
        <style>
        .block-container { padding-top: 0 !important; }

        .navbar {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 58px;
            background: rgba(10, 10, 18, 0.92);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-bottom: 1px solid rgba(255,255,255,0.07);
            position: sticky;
            top: 0;
            z-index: 999;
        }

        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .navbar-brand-icon {
            width: 30px;
            height: 30px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border-radius: 7px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .navbar-brand-text {
            font-size: 15px;
            font-weight: 650;
            color: #ffffff;
            letter-spacing: -0.3px;
        }

        .navbar-brand-text span { color: #818cf8; }
        </style>

        <nav class="navbar">
            <div class="navbar-brand">
                <div class="navbar-brand-icon">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                        <rect x="3" y="3" width="7" height="7" rx="1.5" fill="white"/>
                        <rect x="14" y="3" width="7" height="7" rx="1.5" fill="white" opacity="0.65"/>
                        <rect x="3" y="14" width="7" height="7" rx="1.5" fill="white" opacity="0.65"/>
                        <rect x="14" y="14" width="7" height="7" rx="1.5" fill="white"/>
                    </svg>
                </div>
                <span class="navbar-brand-text">Interview<span>Prep</span></span>
            </div>
        </nav>
    """, unsafe_allow_html=True)