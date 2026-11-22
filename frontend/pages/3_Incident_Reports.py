
import streamlit as st
import requests

from frontend.utils.style import apply_styles

st.set_page_config(
    page_title="MediAI | Hospital Assistant",
    page_icon="🏥",
    layout="wide"
)

apply_styles()
from frontend.utils.api_client import get_incident_report

st.title("📋 Incident Reports")
st.caption("Generate and view hospital incident summary reports.")

if not st.session_state.get("token"):
    st.warning("Please log in first.")
    st.stop()

st.subheader("Hospital Incident Summary Report")

if st.button("Generate Incident Report", type="primary"):
    with st.spinner("Generating incident report..."):
        try:
            response = get_incident_report(st.session_state.token)

            if response.status_code == 200:
                data = response.json()
                report = data.get("report") or data.get("answer") or data.get("result") or data

                if isinstance(report, (dict, list)):
                    report_text = str(report)
                    st.json(report)
                else:
                    report_text = str(report)
                    st.markdown(report_text)

                st.download_button(
                    "Download Report",
                    data=report_text,
                    file_name="hospital_incident_report.txt",
                    mime="text/plain"
                )

            elif response.status_code == 401:
                st.error("Session expired. Please log in again.")
            else:
                st.error(f"API Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as error:
            st.error(f"Could not connect to backend: {error}")
