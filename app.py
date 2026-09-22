import pandas as pd
import streamlit as st
from auth_checker import check_email_access
from prediction_hub import render_prediction_section
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
app_mode = st.sidebar.selectbox(
    "Choose Section:",
    [
        "Prediction Tool",
        "Database & Relational Tables",
        "Subscription Plans",
        "Consultations & Collaboration",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Developer:** Aziza Mnasri(PhD)")
st.sidebar.markdown(
    "**Profile:** Independent Researcher (Organic Chemistry & Computational"
    " Drug Discovery)"
)

if app_mode == "Prediction Tool":
  is_allowed = check_email_access()
  if is_allowed:
    st.markdown("---")
    render_prediction_section()

elif app_mode == "Database & Relational Tables":
  st.markdown("### 🧬 PROTAC Integrated Relational Database")


  @st.cache_data
  def load_relational_data():
    try:
      main_df = pd.read_csv("database.csv")
      warheads_df = pd.read_csv("WARHEADS.csv")
      linkers_df = pd.read_csv("LINKERS.csv")
      e3_df = pd.read_csv("E3_LIGANDS.csv")
      return main_df, warheads_df, linkers_df, e3_df
    except Exception as e:
      st.error(f"Error loading CSV files: {e}")
      return None, None, None, None


  main_df, warheads_df, linkers_df, e3_df = load_relational_data()

  if main_df is not None:
    # دمج الجداول بناءً على الـ IDs المتطابقة
    merged_df = main_df.merge(
        warheads_df, on="Warhead_ID", how="left", suffixes=("", "_warhead")
    )
    merged_df = merged_df.merge(
        linkers_df, on="Linker_ID", how="left", suffixes=("", "_linker")
    )
    merged_df = merged_df.merge(
        e3_df, on="E3_Ligand_ID", how="left", suffixes=("", "_e3")
    )

    tab1, tab2 = st.tabs(
        ["🔗 Complete Merged View", "📂 Raw Sub-tables Viewer"]
    )

    with tab1:
      st.markdown(
          "#### Fully Integrated Table (Main PROTACs + Warheads + Linkers +"
          " E3 Ligands)"
      )
      st.dataframe(merged_df, use_container_width=True)

      csv_data = merged_df.to_csv(index=False).encode("utf-8")
      st.download_button(
          label="📥 Download Complete Database Report (.csv)",
          data=csv_data,
          file_name="integrated_protac_database.csv",
          mime="text/csv",
      )

    with tab2:
      st.markdown("#### Individual Database Tables")
      st.subheader("Main Database (`database.csv`)")
      st.dataframe(main_df)
      st.subheader("Warheads Table (`WARHEADS.csv`)")
      st.dataframe(warheads_df)
      st.subheader("Linkers Table (`LINKERS.csv`)")
      st.dataframe(linkers_df)
      st.subheader("E3 Ligands Table (`E3_LIGANDS.csv`)")
      st.dataframe(e3_df)

elif app_mode == "Subscription Plans":
  render_subscription_section()

elif app_mode == "Consultations & Collaboration":
  render_services_section()
