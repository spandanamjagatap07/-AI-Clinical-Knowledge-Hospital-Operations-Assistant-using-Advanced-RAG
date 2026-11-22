
import streamlit as st
import requests

from frontend.utils.style import apply_styles

st.set_page_config(
    page_title="MediAI | Hospital Assistant",
    page_icon="🏥",
    layout="wide"
)

apply_styles()
from frontend.utils.api_client import get_all_users, create_user

st.title("👥 User Management")
st.caption("Administrator dashboard for managing hospital users.")

if not st.session_state.get("token"):
    st.warning("Please log in first.")
    st.stop()

user = st.session_state.get("user") or {}

if user.get("role") != "admin":
    st.error("Access denied. Only administrators can manage users.")
    st.stop()

token = st.session_state.token

st.subheader("Create Hospital User")

with st.form("create_user_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Temporary Password", type="password")
    role = st.selectbox("Role", ["doctor", "nurse", "admin"])

    submitted = st.form_submit_button("Create User")

if submitted:
    if not username.strip() or not email.strip() or not password:
        st.error("Please complete all fields.")
    elif len(password) < 8:
        st.error("Password must contain at least 8 characters.")
    else:
        try:
            response = create_user(
                token,
                username.strip(),
                email.strip(),
                password,
                role
            )

            if response.status_code in (200, 201):
                st.success("User created successfully!")
                st.json(response.json())
            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as error:
            st.error(f"Backend connection error: {error}")

st.divider()
st.subheader("Registered Hospital Users")

if st.button("Refresh User List"):
    try:
        response = get_all_users(token)

        if response.status_code == 200:
            data = response.json()
            users = data.get("users", data) if isinstance(data, dict) else data

            if isinstance(users, list) and users:
                st.dataframe(users, use_container_width=True)
            else:
                st.info("No users found.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as error:
        st.error(f"Backend connection error: {error}")
