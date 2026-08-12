import streamlit as st

from pages.dashboard import render_dashboard
from pages.analysis import render_analysis
from pages.history import render_history


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Aqua Copilot",
    page_icon="🦐",
    layout="wide"
)


st.title("🦐 Aqua Copilot")
st.caption("AI-Powered Shrimp Pond Intelligence")


page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Pond Analysis",
        "Pond History"
    ]
)


if page == "Dashboard":
    render_dashboard(API_URL)

elif page == "Pond Analysis":
    render_analysis(API_URL)

elif page == "Pond History":
    render_history(API_URL)