
import streamlit as st
import requests

from frontend.utils.api_client import (
    upload_document,
    get_documents,
    delete_document,
    reindex_documents
)

from frontend.utils.style import apply_styles

st.set_page_config(
    page_title="MediAI | Hospital Assistant",
    page_icon="🏥",
    layout="wide"
)

apply_styles()
st.title("📁 Document Management")
st.caption("Upload and manage documents in the hospital knowledge base.")

if not st.session_state.get("token"):
    st.warning("Please log in first.")
    st.stop()

user = st.session_state.get("user") or {}

if user.get("role") != "admin":
    st.error("Only administrators can manage hospital documents.")
    st.stop()

token = st.session_state.token

st.subheader("Upload Hospital Document")

uploaded_file = st.file_uploader(
    "Choose a document",
    type=["txt", "pdf", "docx", "csv", "xlsx", "xls"]
)

if st.button("Upload and Index Document", type="primary"):
    if uploaded_file is None:
        st.warning("Please select a document first.")
    else:
        with st.spinner("Uploading and indexing document..."):
            try:
                response = upload_document(token, uploaded_file)

                if response.status_code == 200:
                    data = response.json()
                    st.success(data.get("message", "Upload successful!"))
                    st.write("Filename:", data.get("filename"))
                    st.write("Chunks created:", data.get("chunks_created"))
                    st.rerun()
                else:
                    st.error(f"Error {response.status_code}: {response.text}")

            except requests.exceptions.RequestException as error:
                st.error(f"Backend connection error: {error}")

st.divider()

st.subheader("Existing Documents")

if st.button("Refresh Document List"):
    st.session_state.show_documents = True

if st.session_state.get("show_documents", True):
    try:
        response = get_documents(token)

        if response.status_code == 200:
            data = response.json()
            documents = data.get("documents", [])

            st.write("Total documents:", data.get("total_documents", 0))

            if documents:
                st.dataframe(documents, use_container_width=True)

                filenames = [doc["filename"] for doc in documents]

                selected_file = st.selectbox(
                    "Select document to delete",
                    filenames
                )

                if st.button("Delete Selected Document"):
                    with st.spinner("Deleting and rebuilding knowledge base..."):
                        delete_response = delete_document(token, selected_file)

                        if delete_response.status_code == 200:
                            st.success("Document deleted successfully!")
                            st.rerun()
                        else:
                            st.error(
                                f"Delete failed: {delete_response.status_code} "
                                f"{delete_response.text}"
                            )
            else:
                st.info("No documents found.")

        else:
            st.error(f"Could not load documents: {response.text}")

    except requests.exceptions.RequestException as error:
        st.error(f"Backend connection error: {error}")

st.divider()

st.subheader("Rebuild Knowledge Base")

if st.button("Re-index All Documents"):
    with st.spinner("Rebuilding Chroma vector database..."):
        try:
            response = reindex_documents(token)

            if response.status_code == 200:
                data = response.json()
                st.success(data.get("message"))
                st.write("Chunks created:", data.get("chunks_created"))
            else:
                st.error(f"Re-indexing failed: {response.text}")

        except requests.exceptions.RequestException as error:
            st.error(f"Backend connection error: {error}")
