
import streamlit as st
import requests
import json

from frontend.utils.style import apply_styles

st.set_page_config(
    page_title="MediAI | Hospital Assistant",
    page_icon="🏥",
    layout="wide"
)

apply_styles()
from frontend.utils.api_client import get_analytics

st.title("📊 Hospital Analytics")
st.caption("Ask questions about hospital operations and structured datasets.")

if not st.session_state.get("token"):
    st.warning("Please log in first.")
    st.stop()

st.subheader("Ask an Analytics Question")

question = st.selectbox(
    "Choose a question",
    [
        "How many patients are registered?",
        "Show appointments by department",
        "Show appointment statistics",
        "Show pharmacy items below reorder level",
        "Show incidents by severity",
        "Show admission statistics",
        "Which department has the most appointments?"
    ]
)

if st.button("Run Analytics", type="primary"):
    with st.spinner("Fetching hospital analytics..."):
        try:
            response = get_analytics(question, st.session_state.token)

            if response.status_code == 200:
                data = response.json()
                st.success("Analytics retrieved successfully!")

                answer = data.get("answer") or data.get("result") or data
                if isinstance(answer, (dict, list)):
                    st.json(answer)
                else:
                    st.markdown(str(answer))

            elif response.status_code == 401:
                st.error("Session expired. Please log in again.")
            else:
                st.error(f"API Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as error:
            st.error(f"Could not connect to backend: {error}")

st.divider()
st.subheader("Enter Your Own Question")

custom_question = st.text_input(
    "Your analytics question",
    placeholder="Example: How many patients are registered?"
)

if st.button("Submit Custom Question"):
    if not custom_question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Processing your question..."):
            try:
                response = get_analytics(
                    custom_question.strip(),
                    st.session_state.token
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer") or data.get("result") or data
                    if isinstance(answer, (dict, list)):
                        st.json(answer)
                    else:
                        st.write(answer)
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")

            except requests.exceptions.RequestException as error:
                st.error(str(error))
