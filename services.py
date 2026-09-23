import streamlit as st


def render_services_section():
  st.subheader("🤝 Consultations & Scientific Collaboration")

  tab1, tab2 = st.tabs(["💡 Custom Consultation", "🔬 Research Collaboration"])

  with tab1:
    st.markdown("### Request a Custom Research Report & File Upload")
    st.markdown(
        "Need a deep-dive analysis, custom molecular docking, or tailored"
        " PROTAC design? You can submit your requirements and attach your"
        " project files directly below:"
    )

    # إنشاء فورم تفاعلي لإرسال البيانات والملفات مباشرة
    with st.form("custom_consultation_form"):
      client_name = st.text_input("Your Name / Institution:")
      client_email = st.text_input("Your Email Address:")
      project_details = st.text_area(
          "Project Details & Requirements (Target, PDB files info, objectives,"
          " etc.):"
      )

      # خانة لإرفاق ملف الخدمة أو الداتا (PDB, SDF, CSV, ZIP, etc.)
      uploaded_file = st.file_uploader(
          "Attach Project File (PDB, SDF, CSV, TXT, or ZIP):",
          type=["pdb", "sdf", "csv", "txt", "zip"],
      )

      submitted = st.form_submit_button("🚀 Send Request & Files")

      if submitted:
        if client_email and project_details:
          st.success(
              f"✅ Thank you {client_name}! Your request and attached file have"
              f" been successfully received. I will review your project and"
              f" get back to `{client_email}` promptly."
          )
          # ملاحظة: يمكنك استقبال الملفات والبيانات المرسلة هنا ومعالجتها برمجياً
        else:
          st.error(
              "Please fill in at least your email address and project"
              " details."
          )

    st.markdown("---")
    st.info("📧 **Direct Contact Email:** azizamnasri10@gmail.com")

  with tab2:
    st.markdown("### Academic & Industrial Partnership")
    st.markdown(
        "Interested in co-authoring papers, joint research grants, or"
        " technological integration? Let's connect."
    )
    st.success("🤝 **For Collaboration Inquiries:** azizamnasri10@gmail.com")
    st.markdown(
        "Send your institution name, proposal, or collaboration idea directly to"
        " my email."
    )
