import streamlit as st

st.set_page_config(page_title="Test App")

st.title("🏥 AI Hospital Assistant")
st.success("Streamlit is working!")

st.header("Login Test")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    st.write("Button is working!")