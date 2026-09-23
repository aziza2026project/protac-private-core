import pandas as pd
import streamlit as st
from auth_checker import check_email_access
from prediction_hub import render_prediction_section
from qrcode_page import render_qrcode_page
from services import render_services_section
from subscription import render_subscription_section

st.set_page_config(
    page_title="PROTAC Prediction & Research Platform",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 PROTAC Research & Prediction Platform")
st.markdown(
    "Welcome to the professional platform for PROTAC design, physicochemical"
    " property calculation, and scientific collaboration."
)

st.sidebar.title("📌 Navigation Menu")
# إضافة خيار QR Code إلى القائمة الجانبية
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
    "**Profile:** Independent Researcher (Organic Chemistry & Computational"
    " Drug Discovery)"
)


# دالة خلفية سرية (Backend Function) لقراءة ودمج الجداول في الكواليس فقط للاستخدام البرمجي
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
