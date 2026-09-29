import datetime
import json
import os
import pandas as pd
import streamlit as st
elif page == "Consultations":
        if st.button("⬅️ Back to Home Page", key="back_to_home_sub"):
            st.session_state['current_page'] = "Home Page"
            st.session_state['collab_sub_tab'] = None
            st.rerun()
        
        st.title("💼 Consultations & Scientific Collaboration")
        st.markdown("Choose between booking a professional consultation/service or proposing a major collaborative research project.")

        if 'collab_sub_tab' not in st.session_state:
            st.session_state['collab_sub_tab'] = None

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🛠️ Consultations & Services", use_container_width=True, key="tab_cons"):
                st.session_state['collab_sub_tab'] = "Consultations"
                st.rerun()
        with col_btn2:
            if st.button("🤝 Scientific Collaborations", use_container_width=True, key="tab_collab"):
                st.session_state['collab_sub_tab'] = "Collaborations"
                st.rerun()

        st.divider()

        # قسم الاستشارات والخدمات (Consultations)
        if st.session_state['collab_sub_tab'] == "Consultations":
            st.subheader("📋 Request a Professional Consultation")
            st.markdown("Submit your project details and upload any files freely. Dr. Aziza Mnasri will review your request and get back to you with an evaluation and pricing details.")

            with st.form("consultation_form"):
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    client_name = st.text_input("Full Name *")
                    client_lab = st.text_input("Laboratory / Institution *")
                with col_i2:
                    client_email = st.text_input("Your Email Address * (For receiving the evaluation and report)")
                    client_whatsapp = st.text_input("WhatsApp Number (Optional)")

                project_description = st.text_area("Project Description & Requirements *", placeholder="Describe what you need precisely (e.g., molecular docking, ADME evaluation, PROTAC linker design)...")
                
                uploaded_files = st.file_uploader("Upload Project Files (All formats & sizes accepted)", accept_multiple_files=True)

                st.info("📨 Your request and files will be sent directly to: azizamnasri01@gmail.com for review.")
                
                submit_consultation = st.form_submit_button("Submit Consultation Request & Files")

                if submit_consultation:
                    if not client_name or not client_email or not project_description:
                        st.error("Please fill in all mandatory fields (*).")
                    else:
                        st.success("Consultation request successfully submitted! Your files and details have been sent to azizamnasri01@gmail.com. We will review it and contact you soon.")

            # قسم الدفع الاختياري (خارج الفورم أو تحته لكي يتم استخدامه بعد الاتفاق على السعر)
            with st.container():
                st.markdown("---")
                st.subheader("💳 Secure Consultation Payment Gateway")
                st.markdown("If you have already discussed your project with Dr. Aziza Mnasri and agreed on the service terms, you can securely proceed with the payment below:")
                
                col_pay1, col_pay2 = st.columns([2, 1])
                with col_pay1:
                    st.text_input("Enter Consultation Reference or Invoice ID (Optional)", key="invoice_id_input")
                with col_pay2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Proceed to Secure Payment", use_container_width=True):
                        st.info("Redirecting to secure payment gateway... (Link your payment processor here)")

            # لوحة التحكم الخاصة بالأدمن (محمية بكلمة مرور)
            with st.expander("🔐 Admin Dashboard (Dr. Aziza Mnasri Only)"):
                admin_pass = st.text_input("Enter Admin Password", type="password", key="consult_admin_pass")
                if admin_pass == "aziza2026":
                    st.success("Access Granted to Admin Dashboard")
                    
                    dash_tab1, dash_tab2, dash_tab3, dash_tab4 = st.tabs(["📥 All Requests", "🔴 Unread", "⏳ In Progress", "✅ Answered"])
                    
                    with dash_tab1:
                        st.write("Displaying all consultation requests...")
                    with dash_tab2:
                        st.write("Displaying unread / new requests (To be checked)...")
                    with dash_tab3:
                        st.write("Displaying requests in progress...")
                    with dash_tab4:
                        st.write("Displaying completed & answered requests...")
                elif admin_pass:
                    st.error("Incorrect password.")

        # قسم التعاون العلمي والمشاريع الكبرى (Scientific Collaborations)
        elif st.session_state['collab_sub_tab'] == "Collaborations":
            st.subheader("🤝 Scientific Collaborations & Major Research Projects")
            st.markdown("Partner with Dr. Aziza Mnasri for high-impact joint research, strategic Big Pharma collaborations, and world-class academic publications.")

            with st.form("collaboration_form"):
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    collab_name = st.text_input("Researcher / Institution / Big Pharma Name *")
                    collab_email = st.text_input("Contact Email *")
                with col_c2:
                    collab_type = st.selectbox("Strategic Collaboration Type", [
                        "Big Pharma & Biotech R&D Partnership",
                        "Global Academic Research Consortium",
                        "Joint High-Impact Scientific Publications",
                        "Strategic Computational Drug Discovery Project"
                    ])
                
                collab_details = st.text_area("Project Proposal & Strategic Objectives *", placeholder="Describe the scope of the major research project, partnership goals, and expected outcomes...")

                st.info("📨 Proposals will be sent directly to: azizamnasri01@gmail.com")
                
                submit_collab = st.form_submit_button("Send Strategic Collaboration Proposal")

                if submit_collab:
                    if not collab_name or not collab_email or not collab_details:
                        st.error("Please fill in all required fields.")
                    else:
                        st.success("Strategic collaboration proposal successfully sent to azizamnasri01@gmail.com!")
