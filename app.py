import streamlit as st
from auth_checker import check_email_access
from prediction_hub import render_prediction_section
from subscription import render_subscription_section
from services import render_services_section

st.set_page_config(
    page_title="PROTAC Prediction & Research Platform",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 PROTAC Research & Prediction Platform")
st.markdown("Welcome to the professional platform for PROTAC design, physicochemical property calculation, and scientific collaboration.")

st.sidebar.title("📌 Navigation Menu")
app_mode = st.sidebar.selectbox(
    "Choose Section:",
    ["Prediction Tool", "Subscription Plans", "Consultations & Collaboration"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Developer:** Aziza Mnasri(PhD)")
st.sidebar.markdown("**Profile:** Independent Researcher (Organic Chemistry & Computational Drug Discovery)")

if app_mode == "Prediction Tool":
    is_allowed = check_email_access()
    if is_allowed:
        st.markdown("---")
        render_prediction_section()

elif app_mode == "Subscription Plans":
    render_subscription_section()

elif app_mode == "Consultations & Collaboration":
    render_services_section()
