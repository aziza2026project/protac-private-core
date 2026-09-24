import io
import pandas as pd
import qrcode
import streamlit as st
from auth_checker import check_email_access
from prediction_hub import render_prediction_section, render_ai_prediction_hub
from services import render_services_section
from subscription import render_subscription_section

st.set_page_config(
    page_title="PROTAC Prediction & Research Platform",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 PROTAC Research & Prediction Platform")
st.markdown(
    "Welcome to the professional platform for PROTAC design, physicochemical "
    "property calculation, and scientific collaboration."
)

st.sidebar.title("📌 Navigation Menu")
app_mode = st.sidebar.selectbox(
    "Choose Section:",
    [
        "Prediction Tool",
        "Subscription Plans",
        "Consultations & Collaboration",
        "📱 App QR Code",
        "🤖 Developer AI Hub (Protected)",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Developer:** Aziza Mnasri (PhD)")
st.sidebar.markdown(
    "**Profile:** Independent Researcher (Organic Chemistry & Computational "
    "Drug Discovery)"
)

# =========================================================================
# MAIN APP ROUTING
# =========================================================================
if app_mode == "Prediction Tool":
    is_allowed = check_email_access()
    if is_allowed:
        st.markdown("---")
        render_prediction_section()

elif app_mode == "Subscription Plans":
    render_subscription_section()

elif app_mode == "Consultations & Collaboration":
    render_services_section()

elif app_mode == "📱 App QR Code":
    render_qrcode_page()

elif app_mode == "🤖 Developer AI Hub (Protected)":
    st.markdown("---")
    st.markdown("### 🔐 Developer Authentication Required")
    dev_password = st.text_input("Enter Developer Password:", type="password", key="dev_page_pass")
    CORRECT_PASSWORD = "aziza_protac_2026"
    
    if dev_password == CORRECT_PASSWORD:
        st.success("Access Granted! Welcome to the AI & QSAR Prediction Hub.")
        st.markdown("---")
        render_ai_prediction_hub()
    elif dev_password != "":
        st.error("Incorrect password. Access denied.")
    else:
        st.info("Please enter the password to access the advanced AI prediction features.")
