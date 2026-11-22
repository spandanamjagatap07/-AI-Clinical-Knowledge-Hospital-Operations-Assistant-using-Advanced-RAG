import streamlit as st
import requests

from frontend.utils.api_client import (
    register_user,
    login_user,
    logout_user,
)

from frontend.utils.style import apply_styles


# =========================================================
# PAGE CONFIGURATION
# Keep this ONCE, and keep it before other Streamlit calls.
# =========================================================

st.set_page_config(
    page_title="MediAI | Hospital Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load the shared design on this page.
apply_styles()


# =========================================================
# SESSION STATE
# =========================================================

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "auth_message" not in st.session_state:
    st.session_state.auth_message = ""


# =========================================================
# BRANDING
# =========================================================

def display_brand():
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="
                background:#1677c8;
                padding:10px;
                border-radius:12px;
                font-size:27px;">
                🏥
            </div>
            <div>
                <div style="
                    font-size:25px;
                    font-weight:800;
                    color:#17324d;">
                    MediAI
                </div>
                <div style="
                    font-size:12px;
                    color:#64748b;">
                    INTELLIGENT HOSPITAL ASSISTANT
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# LOGIN AND REGISTRATION
# =========================================================

def authentication_page():
    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.05, 1.1], gap="large")

    with left:
        st.markdown(
            """
            <div class="hero-card">
                <div class="hero-tag">✦ AI POWERED HEALTHCARE</div>
                <h1>Smarter Healthcare.<br>Better Decisions.</h1>
                <p>
                    Your intelligent hospital assistant for clinical
                    knowledge, hospital operations, incident management
                    and healthcare analytics.
                </p>
                <br>
                <div style="font-size:15px;color:white;">
                    ✓ Clinical Knowledge Assistance<br><br>
                    ✓ Hospital Data Analytics<br><br>
                    ✓ Intelligent Incident Reporting<br><br>
                    ✓ Secure User Authentication
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown("<br>", unsafe_allow_html=True)
        display_brand()
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("### Welcome Back!")
        st.caption("Sign in to access your hospital workspace.")

        if st.session_state.auth_message:
            st.success(st.session_state.auth_message)
            st.session_state.auth_message = ""

        login_tab, register_tab = st.tabs(["🔐 Login", "👤 Register"])

        with login_tab:
            st.markdown("#### Sign in to your account")

            with st.form("login_form"):
                username = st.text_input(
                    "Username",
                    placeholder="Enter your username",
                )
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                )
                login_button = st.form_submit_button(
                    "Sign In →",
                    use_container_width=True,
                )

            if login_button:
                if not username.strip() or not password:
                    st.error("Please enter username and password.")
                else:
                    try:
                        response = login_user(username.strip(), password)

                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.token = data["access_token"]
                            st.session_state.user = data["user"]
                            st.rerun()
                        else:
                            try:
                                detail = response.json().get(
                                    "detail", "Login failed."
                                )
                            except ValueError:
                                detail = "Login failed."
                            st.error(detail)

                    except requests.exceptions.ConnectionError:
                        st.error(
                            "Cannot connect to FastAPI. "
                            "Please start the backend server."
                        )
                    except requests.exceptions.RequestException:
                        st.error("Unable to contact the backend.")
                    except (ValueError, KeyError):
                        st.error("Unexpected response from the backend.")

        with register_tab:
            st.markdown("#### Create your account")
            st.info(
                "Public registration creates accounts with the Nurse role."
            )

            with st.form("register_form"):
                new_username = st.text_input(
                    "Choose Username",
                    key="register_username",
                    placeholder="Enter username",
                )
                new_email = st.text_input(
                    "Email Address",
                    key="register_email",
                    placeholder="Enter email address",
                )
                new_password = st.text_input(
                    "Create Password",
                    type="password",
                    key="register_password",
                    placeholder="Minimum 8 characters",
                )
                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter password",
                )
                register_button = st.form_submit_button(
                    "Create Account →",
                    use_container_width=True,
                )

            if register_button:
                if not new_username.strip() or not new_email.strip():
                    st.error("Please complete all fields.")
                elif len(new_password) < 8:
                    st.error("Password must contain at least 8 characters.")
                elif len(new_password) > 128:
                    st.error("Password cannot exceed 128 characters.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    try:
                        response = register_user(
                            new_username.strip(),
                            new_email.strip(),
                            new_password,
                        )

                        if response.status_code == 201:
                            st.session_state.auth_message = (
                                "Registration successful! You can now log in."
                            )
                            st.rerun()
                        else:
                            try:
                                detail = response.json().get(
                                    "detail", "Registration failed."
                                )
                            except ValueError:
                                detail = "Registration failed."
                            st.error(detail)

                    except requests.exceptions.ConnectionError:
                        st.error(
                            "Cannot connect to FastAPI. "
                            "Please start the backend server."
                        )
                    except requests.exceptions.RequestException:
                        st.error("Unable to contact the backend.")
                    except ValueError:
                        st.error("Unexpected response from the backend.")

        st.markdown(
            """
            <div class="footer">
                © 2026 MediAI Hospital Assistant<br>
                Intelligent Healthcare Management Platform
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# DASHBOARD
# =========================================================

def dashboard_page():
    user = st.session_state.user or {}
    username = user.get("username", "User")

    # Intentionally no account/profile information in the sidebar.
    # Streamlit's multipage navigation is generated from frontend/pages.

    with st.sidebar:
        st.markdown(
            """
            <div style="
                background:rgba(255,255,255,0.13);
                padding:12px;
                border-radius:9px;
                color:#ffffff;
                font-weight:700;">
                🏠 &nbsp; Dashboard
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()

    st.markdown(
        f"""
        <div class="welcome-banner">
            <div style="font-size:13px;letter-spacing:1px;">
                HOSPITAL MANAGEMENT WORKSPACE
            </div>
            <h2>Welcome back, {username}! 👋</h2>
            <p>
                Your intelligent hospital assistant is ready.
                Manage clinical knowledge and hospital operations
                from one workspace.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🏥 Dashboard Overview")
    st.caption("Access your hospital's intelligent management modules.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="card-icon">💬</div>
                <h3>Clinical Chat</h3>
                <p>Ask clinical questions and retrieve information from hospital documents.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="card-icon">📊</div>
                <h3>Hospital Analytics</h3>
                <p>Explore hospital data, appointments, departments and operational insights.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="card-icon">🚨</div>
                <h3>Incident Reports</h3>
                <p>Generate incident summaries and review hospital safety information.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="card-icon">📁</div>
                <h3>Document Management</h3>
                <p>Access and manage hospital documents and clinical knowledge resources.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col5:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="card-icon">👥</div>
                <h3>User Management</h3>
                <p>Manage hospital accounts and role-based user access.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col6:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="card-icon">🤖</div>
                <h3>AI Assistant</h3>
                <p>Use intelligent AI capabilities to support hospital operations.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="footer">
            MediAI | AI-Powered Hospital Management System
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

if st.session_state.token:
    dashboard_page()
else:
    authentication_page()
