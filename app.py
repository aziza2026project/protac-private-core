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

# Custom CSS for perfect alignment, smaller balanced headers, and sleek styling
st.markdown("""
    <style>
    /* Styling the buttons */
    .stButton>button {
        background-color: #1f4e78;
        color: white;
        border-radius: 6px;
        font-weight: 600;
        border: none;
        width: 100%;
        padding: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #16385c;
        color: white;
    }
    
    /* Balanced headers for the 3 main cards */
    .card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1f4e78;
        margin-bottom: 1rem;
        min-height: 3rem;
        display: flex;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if "active_page" not in st.session_state:
    st.session_state.active_page = "home"

# =========================================================================
# CLEAN SIDEBAR
# =========================================================================
st.sidebar.title("📌 Quick Navigation")

if st.sidebar.button("🏠 Home Page", use_container_width=True):
    st.session_state.active_page = "home"
    st.rerun()

if st.sidebar.button("📱 View App QR Code", use_container_width=True):
    st.session_state.active_page = "qr_code"
    st.rerun()

st.sidebar.markdown("---")

# Developer & AI Hub Access Expander
with st.sidebar.expander("⚙️ Developer & AI Hub Access"):
    dev_password = st.text_input("Password:", type="password", key="sidebar_dev_pass")
    CORRECT_PASSWORD = "aziza_protac_2026"
    
    if dev_password == CORRECT_PASSWORD:
        st.session_state.is_developer = True
    else:
        if dev_password != "":
            st.sidebar.error("Incorrect Password")
        st.session_state.is_developer = False

is_developer = st.session_state.get("is_developer", False)

st.sidebar.markdown("---")
st.sidebar.markdown("**Developer:** Aziza Mnasri (PhD)")
st.sidebar.markdown(
    "**Profile:** Independent Researcher (Organic Chemistry & Computational "
    "Drug Discovery)"
)

# =========================================================================
# MAIN APP HEADER
# =========================================================================
st.title("🧬 PROTAC Research & Prediction Platform")
st.markdown(
    "Welcome to the professional platform for PROTAC design, physicochemical "
    "property calculation, and scientific collaboration."
)
st.markdown("---")

# =========================================================================
# PAGES DEFINITION
# =========================================================================

def render_home_page():
    st.markdown("## 🌟 Welcome to PROTAC Research Hub")
    st.markdown("Choose a section below to get started with your research, design, and collaboration workflow:")
    st.markdown("")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card-title">💳 Subscription Plans</div>', unsafe_allow_html=True)
        if st.button("Open Subscriptions", key="btn_sub"):
            st.session_state.active_page = "subscription"
            st.rerun()
            
    with col2:
        st.markdown('<div class="card-title">🔬 Prediction Tool</div>', unsafe_allow_html=True)
        if st.button("Open Prediction Tool", key="btn_pred"):
            st.session_state.active_page = "prediction"
            st.rerun()
            
    with col3:
        st.markdown('<div class="card-title">🤝 Consultations & Collaboration</div>', unsafe_allow_html=True)
        if st.button("Open Consultations", key="btn_serv"):
            st.session_state.active_page = "consultations"
            st.rerun()

    # Advanced AI Hub ONLY shows on home page if developer mode is unlocked via sidebar password
    if is_developer:
        st.markdown("---")
        render_ai_prediction_hub()


def render_qrcode_page():
    st.markdown("## 📱 Web App QR Code & Access Hub")
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    app_url = "https://protac-app-core.streamlit.app"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(app_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    with col1:
        st.markdown("### 📌 Direct Link")
        st.info(f"🔗 `{app_url}`")
        st.markdown("### 📥 Download")
        st.download_button(
            label="📥 Download QR Code (PNG)",
            data=byte_im,
            file_name="PROTAC_Platform_QRCode.png",
            mime="image/png",
        )
    with col2:
        st.markdown("### 👁️ Live Preview")
        st.image(byte_im, width=220)


# =========================================================================
# ROUTING LOGIC
# =========================================================================
if st.session_state.active_page == "home":
    render_home_page()

elif st.session_state.active_page == "subscription":
    if st.button("← Back to Home"):
        st.session_state.active_page = "home"
        st.rerun()
    render_subscription_section()

elif st.session_state.active_page == "prediction":
    if st.button("← Back to Home"):
        st.session_state.active_page = "home"
        st.rerun()
    is_allowed = check_email_access()
    if is_allowed:
        render_prediction_section()
        if is_developer:
            st.markdown("---")
            render_ai_prediction_hub()

elif st.session_state.active_page == "consultations":
    if st.button("← Back to Home"):
        st.session_state.active_page = "home"
        st.rerun()
    render_services_section()

elif st.session_state.active_page == "qr_code":
    if st.button("← Back to Home"):
        st.session_state.active_page = "home"
        st.rerun()
    render_qrcode_page()
