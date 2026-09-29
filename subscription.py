import pandas as pd
import streamlit as st
def render_subscriptions_page():
    if st.button("⬅️ Back to Home Page", key="back_to_home_sub"):
        st.session_state['current_page'] = "Home Page"
        st.rerun()
        
    st.title("💳 Subscription Plans & Research Tiers")
    st.markdown("Choose the appropriate computational tier for your target research, PROTAC design, and molecular docking workflows.")
    st.info("Current Status: Professional Researcher Access Active.")

    st.markdown("---")
    
    col_sub1, col_sub2, col_sub3 = st.columns(3)

    with col_sub1:
        st.subheader("🌱 Starter Tier")
        st.markdown("**Free / Academic**")
        st.markdown("""
        - Basic ADME & Pharmacokinetics (pkCSM)
        - Standard Molecular Docking Preview
        - Community Support
        - Ideal for students and academic exploration
        """)
        st.button("Current Tier", key="btn_tier_free", disabled=True, use_container_width=True)

    with col_sub2:
        st.subheader("⚡ Professional Tier")
        st.markdown("**$49 / month**")
        st.markdown("""
        - Full AutoDock Vina Docking Workspaces
        - Advanced Linker Optimization & Flexibility
        - Priority Queue for Calculations
        - Designed for active researchers & PROTAC developers
        """)
        if st.button("Upgrade to Professional", key="btn_tier_pro", use_container_width=True):
            st.success("Redirecting to secure subscription checkout...")

    with col_sub3:
        st.subheader("🚀 Enterprise & Lab Tier")
        st.markdown("**Custom / Institutional**")
        st.markdown("""
        - Unlimited High-Performance Docking
        - Custom Target Proteins & Dual-Target PROTACs
        - Dedicated Scientific Consultation & Support
        - Tailored for Biotech R&D Labs & Pharma
        """)
        if st.button("Contact for Enterprise", key="btn_tier_ent", use_container_width=True):
            st.info("Please switch to the 'Consultations & Collaboration' page to connect directly.")
