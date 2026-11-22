
import streamlit as st


def apply_styles():

    st.markdown("""
    <style>

    /* =====================================
       GLOBAL APPLICATION THEME
    ===================================== */

    .stApp {
        background-color: #f4f7fb !important;
        color: #17324d !important;
        font-size: 18px !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1450px !important;
    }

    /* =====================================
       ALL PAGE HEADINGS
    ===================================== */

    h1 {
        font-size: 38px !important;
        font-weight: 800 !important;
        color: #17324d !important;
    }

    h2 {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #17324d !important;
    }

    h3 {
        font-size: 25px !important;
        font-weight: 700 !important;
        color: #17324d !important;
    }

    p, label, .stMarkdown {
        font-size: 18px !important;
        line-height: 1.7 !important;
    }

    /* =====================================
       SIDEBAR - PERMANENT NAVY BLUE
    ===================================== */

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        background-color: #102a43 !important;
        color: #ffffff !important;
    }

    /* Sidebar navigation container */

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        background-color: #102a43 !important;
        padding-top: 15px !important;
    }

    /* Navigation links */

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {
        background-color: transparent !important;
        color: #ffffff !important;
        font-size: 19px !important;
        font-weight: 600 !important;
        min-height: 48px !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
    }

    /* Navigation text */

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a *,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] * {
        color: #ffffff !important;
        font-size: 19px !important;
        font-weight: 600 !important;
    }

    /* Selected navigation item */

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {
        background-color: #1677c8 !important;
        color: #ffffff !important;
        border-left: 4px solid #ffffff !important;
    }

    /* Selected navigation text */

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] *,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] * {
        color: #ffffff !important;
        font-size: 19px !important;
    }

    /* Navigation hover */

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {
        background-color: #1b4968 !important;
        color: #ffffff !important;
    }

    /* Keep sidebar contents white */

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: #ffffff;
    }

    /* Sidebar buttons */

    section[data-testid="stSidebar"] .stButton button {
        background-color: #1677c8 !important;
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 9px !important;
        padding: 12px !important;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #105b9c !important;
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.25) !important;
    }

    /* =====================================
       MAIN BUTTONS
    ===================================== */

    .stButton button,
    .stFormSubmitButton button {
        background-color: #1677c8 !important;
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        border-radius: 9px !important;
        padding: 12px 18px !important;
    }

    .stButton button:hover,
    .stFormSubmitButton button:hover {
        background-color: #105b9c !important;
        color: #ffffff !important;
    }

    /* =====================================
       INPUT FIELDS
    ===================================== */

    .stTextInput input,
    .stTextArea textarea {
        font-size: 18px !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }

    .stTextInput label,
    .stTextArea label {
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    /* =====================================
       TABS
    ===================================== */

    .stTabs [data-baseweb="tab"] {
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    /* =====================================
       ALERTS AND CAPTIONS
    ===================================== */

    [data-testid="stAlert"] {
        font-size: 17px !important;
    }

    [data-testid="stCaptionContainer"] {
        font-size: 16px !important;
    }

    /* =====================================
       RESPONSIVE DESIGN
    ===================================== */

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem !important;
        }

        h1 {
            font-size: 30px !important;
        }

        h2 {
            font-size: 26px !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)
