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
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Developer:** Aziza Mnasri (PhD)")
st.sidebar.markdown(
    "**Profile:** Independent Researcher (Organic Chemistry & Computational "
    "Drug Discovery)"
)

# =========================================================================
# SECURE DEVELOPER ACCESS (Hidden in Sidebar Expander - Only for You)
# =========================================================================
st.sidebar.markdown("---")
unlock_ai = False
with st.sidebar.expander("⚙️ Developer & AI Hub Access"):
    dev_password = st.text_input("Enter Password:", type="password", key="sidebar_dev_pass")
    CORRECT_PASSWORD = "aziza_protac_2026"
    
    if dev_password == CORRECT_PASSWORD:
        st.success("Access Granted!")
        unlock_ai = True
    else:
        if dev_password != "":
            st.error("Incorrect password")
        unlock_ai = False


@st.cache_data
def get_integrated_protac_database():
  try:
    main_df = pd.read_csv("database.csv")
    warheads_df = pd.read_csv("WARHEADS.csv")
    linkers_df = pd.read_csv("LINKERS.csv")
    e3_df = pd.read_csv("E3_LIGANDS.csv")

    merged_df = main_df.merge(
        warheads_df, on="Warhead_ID", how="left", suffixes=("", "_warhead")
    )
    merged_df = merged_df.merge(
        linkers_df, on="Linker_ID", how="left", suffixes=("", "_linker")
    )
    merged_df = merged_df.merge(
        e3_df, on="E3_Ligand_ID", how="left", suffixes=("", "_e3")
    )
    return merged_df
  except Exception:
    return None


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
# MAIN APP ROUTING
# =========================================================================
if unlock_ai:
    st.markdown("---")
    # If you enter the password in the sidebar, the AI Hub opens up cleanly here!
    render_ai_prediction_hub()
else:
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
