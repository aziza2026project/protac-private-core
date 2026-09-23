import datetime
import pandas as pd
import streamlit as st


def render_services_section():
  st.subheader("🤝 Consultations & Scientific Collaboration")

  # تهيئة صندوق الوارد في الذاكرة لتخزين الطلبات
  if "client_requests" not in st.session_state:
    st.session_state.client_requests = []

  tab1, tab2, tab3 = st.tabs([
      "💡 Custom Consultation",
      "🔬 Research Collaboration",
      "🔐 Admin Portal",
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
          request_data = {
              "name": client_name if client_name else "Anonymous",
              "email": client_email,
              "details": project_details,
              "file": uploaded_file,
              "timestamp": datetime.datetime.now().strftime(
                  "%Y-%m-%d %H:%M"
              ),  # توقيت الإرسال
              "is_read": False,  # حالة القراءة
              "is_responded": False,  # حالة الإجابة
          }
          # إدخال الطلب الجديد في أول القائمة
          st.session_state.client_requests.insert(0, request_data)

          st.success(
              f"✅ Thank you {client_name}! Your request and file have been"
              " successfully saved."
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
    st.markdown("### 🔐 Admin Secure Inbox")
    admin_password = st.text_input(
        "Admin Password:", type="password", key="admin_pass_input"
    )

    if admin_password == "aziza2026":
      st.success("🔓 Access Granted: Welcome to your secure inbox.")

      if len(st.session_state.client_requests) == 0:
        st.info("📭 Your inbox is currently empty. No new requests received.")
      else:
        # إحصائيات سريعة للطلبات
        total = len(st.session_state.client_requests)
        unread = sum(
            1 for r in st.session_state.client_requests if not r["is_read"]
        )
        responded = sum(
            1 for r in st.session_state.client_requests if r["is_responded"]
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Requests", total)
        col2.metric("Unread", unread)
        col3.metric("Responded", responded)

        st.markdown("---")

        for idx, req in enumerate(st.session_state.client_requests):
          # تحديد الأيقونة حسب الحالة
          if req["is_responded"]:
            status_icon = "✅"
          elif not req["is_read"]:
            status_icon = "🆕"
          else:
            status_icon = "👁️"

          title_str = (
              f"{status_icon} Request #{total - idx} | {req['name']}"
              f" ({req['email']}) — [{req['timestamp']}]"
          )

          with st.expander(title_str):
            # بمجرد فتح الطلب، يصبح مقروءاً تلقائياً
            if not req["is_read"]:
              req["is_read"] = True

            st.markdown(f"**🕒 Time:** {req['timestamp']}")
            st.markdown(f"**👤 Client Name:** {req['name']}")
            st.markdown(f"**📧 Email:** {req['email']}")
            st.markdown(f"**📝 Project Details:**\n{req['details']}")

            if req["file"] is not None:
              st.markdown(f"**📎 Attached File:** `{req['file'].name}`")
              st.download_button(
                  label=f"📥 Download {req['file'].name}",
                  data=req["file"],
                  file_name=req['file'].name,
                  key=f"secure_download_btn_{idx}",
              )
            else:
              st.markdown("*No file attached with this request.*")

            st.markdown("---")
            # أزرار لتغيير الحالة أو الحذف
            c1, c2 = st.columns(2)
            with c1:
              if not req["is_responded"]:
                if st.button(
                    "✔️ Mark as Responded", key=f"resp_btn_{idx}"
                ):
                  req["is_responded"] = True
                  st.rerun()
              else:
                if st.button("🔄 Mark as Unanswered", key=f"unresp_btn_{idx}"):
                  req["is_responded"] = False
                  st.rerun()
            with c2:
              if st.button("🗑️ Delete Request", key=f"del_req_{idx}"):
                st.session_state.client_requests.pop(idx)
                st.rerun()

    elif admin_password:
      st.error("❌ Incorrect password. Access denied.")
    else:
      st.warning("⚠️ Please enter your password to view the requests.")
