import pandas as pd
import streamlit as st


def render_services_section():
  st.subheader("🤝 Consultations & Scientific Collaboration")

  # تهيئة صندوق الوارد في الذاكرة لتخزين الطلبات والملفات
  if "client_requests" not in st.session_state:
    st.session_state.client_requests = []

  tab1, tab2, tab3 = st.tabs([
      "💡 Custom Consultation",
      "🔬 Research Collaboration",
      "📥 Admin Inbox (Client Requests)",
  ])

  with tab1:
    st.markdown("### Request a Custom Research Report & File Upload")
    st.markdown(
        "Need a deep-dive analysis, custom molecular docking, or tailored"
        " PROTAC design? Submit your requirements and attach your project files"
        " directly:"
    )

    with st.form("custom_consultation_form"):
      client_name = st.text_input("Your Name / Institution:")
      client_email = st.text_input("Your Email Address:")
      project_details = st.text_area(
          "Project Details & Requirements (Target, PDB files info, objectives,"
          " etc.):"
      )

      uploaded_file = st.file_uploader(
          "Attach Project File (PDB, SDF, CSV, TXT, or ZIP):",
          type=["pdb", "sdf", "csv", "txt", "zip"],
      )

      submitted = st.form_submit_button("🚀 Send Request & Files")

      if submitted:
        if client_email and project_details:
          # حفظ الطلب والملف في صندوق الوارد المحلي
          request_data = {
              "name": client_name if client_name else "Anonymous",
              "email": client_email,
              "details": project_details,
              "file": uploaded_file,  # تخزين الملف المرفق
          }
          st.session_state.client_requests.append(request_data)

          st.success(
              f"✅ Thank you {client_name}! Your request and file have been"
              " successfully saved. I will check them in my inbox."
          )
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

  with tab3:
    st.markdown("### 📥 Received Client Requests & Files")
    st.markdown(
        "Here you can view all project requests and download files sent by"
        " clients:"
    )

    if len(st.session_state.client_requests) == 0:
      st.info(
          "📭 Your inbox is currently empty. No new requests have been"
          " submitted yet."
      )
    else:
      for idx, req in enumerate(st.session_state.client_requests):
        with st.expander(
            f"📌 Request #{idx+1} from {req['name']} ({req['email']})"
        ):
          st.markdown(f"**Client Name:** {req['name']}")
          st.markdown(f"**Email:** {req['email']}")
          st.markdown(f"**Project Details:**\n{req['details']}")

          if req["file"] is not None:
            st.markdown(f"**Attached File:** `{req['file'].name}`")
            # زر لتحميل الملف المرفق من قبل العميل
            st.download_button(
                label=f"📥 Download {req['file'].name}",
                data=req["file"],
                file_name=req["file"].name,
                key=f"download_btn_{idx}",
            )
          else:
            st.markdown("*No file attached with this request.*")
