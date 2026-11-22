
import streamlit as st
import requests
import json

from frontend.utils.api_client import chat_with_assistant

from frontend.utils.style import apply_styles

st.set_page_config(
    page_title="MediAI | Hospital Assistant",
    page_icon="🏥",
    layout="wide"
)

apply_styles()
st.title("💬 Clinical Chat")
st.caption("Ask questions about hospital SOPs, clinical guidelines and nursing protocols.")

# Check login
if not st.session_state.get("token"):
    st.warning("Please log in from the main dashboard first.")
    st.stop()

# Initialize chat history
if "clinical_chat_history" not in st.session_state:
    st.session_state.clinical_chat_history = []

# Clear conversation
if st.button("🗑️ Clear Conversation"):
    st.session_state.clinical_chat_history = []
    st.rerun()

st.divider()

# Display previous messages
for message in st.session_state.clinical_chat_history:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask a question about hospital procedures...")

if question:

    # Display user question
    st.session_state.clinical_chat_history.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Searching hospital knowledge base and generating answer..."):

            try:
                response = chat_with_assistant(
                    question,
                    st.session_state.token
                )

                if response.status_code == 200:

                    data = response.json()

                    # Handle different possible response field names
                    answer = (
                        data.get("answer")
                        or data.get("response")
                        or data.get("result")
                    )

                    if answer is None:
                        answer = json.dumps(data, indent=2)

                    st.markdown(str(answer))

                    st.session_state.clinical_chat_history.append({
                        "role": "assistant",
                        "content": str(answer)
                    })

                elif response.status_code == 401:
                    st.error("Your login session has expired. Please log in again.")

                else:
                    try:
                        error_detail = response.json().get(
                            "detail",
                            "Something went wrong."
                        )
                    except ValueError:
                        error_detail = response.text

                    st.error(f"API Error ({response.status_code}): {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI. Please check whether the backend is running.")

            except requests.exceptions.Timeout:
                st.error("The request took too long. Please try again.")

            except requests.exceptions.RequestException as error:
                st.error(f"Request failed: {error}")

            except ValueError:
                st.error("The backend returned an invalid response.")
