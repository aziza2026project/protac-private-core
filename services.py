import datetime
import pandas as pd
import streamlit as st


def render_services_section():
  st.subheader("🤝 Consultations & Scientific Collaboration")

  # تهيئة صندوق الوارد في الذاكرة لضمان حفظ الطلبات
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

    with st.form("custom_consultation_form", clear_on_submit=True):
      client_name = st.text_input("Your Name / Institution:")
      client_email = st.text_input("Your Email Address:")
      project_details = st.text_area(
          "Project Details & Requirements (Target, PDB files info, objectives,"
          " etc.):"
      )

      # تم إضافة accept_multiple_files=True لقبول عدة ملفات في نفس الريكويست
      uploaded_files = st.file_uploader(
          "Attach Project Files (PDF, PDB, ZIP, TXT, Word, etc.):",
          accept_multiple_files=True,
      )

      submitted = st.form_submit_button("🚀 Send Request & Files")

      if submitted:
        if client_email and project_details:
          request_data = {
              "name": client_name if client_name else "Anonymous",
              "email": client_email,
              "details": project_details,
              "files": uploaded_files,  # حفظ قائمة الملفات المرفقة
              "timestamp": datetime.datetime.now().strftime(
                  "%Y-%m-%d %H:%M:%S"
              ),
              "is_read": False,
              "is_responded": False,
          }
          st.session_state.client_requests.append(request_data)

          st.success(
              f"✅ Thank you {client_name}! Your request and files have been"
              " successfully saved in the inbox."
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
        requests_reversed = list(enumerate(st.session_state.client_requests))[
            ::-1
        ]

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

        for idx, req in requests_reversed:
          if req["is_responded"]:
            status_icon = "✅"
          elif not req["is_read"]:
            status_icon = "🆕"
          else:
            status_icon = "👁️"

          title_str = (
              f"{status_icon} Request #{idx+1} | {req['name']}"
              f" ({req['email']}) — [{req['timestamp']}]"
          )

          with st.expander(title_str):
            st.session_state.client_requests[idx]["is_read"] = True

            st.markdown(f"**🕒 Time:** {req['timestamp']}")
            st.markdown(f"**👤 Client Name:** {req['name']}")
            st.markdown(f"**📧 Email:** {req['email']}")
            st.markdown(f"**📝 Project Details:**\n{req['details']}")

            # عرض وتحميل الملفات المتعددة إن وجدت
            if req["files"] and len(req["files"]) > 0:
              st.markdown(
                  f"**📎 Attached Files ({len(req['files'])} files):**"
              )
              for f_idx, file_obj in enumerate(req["files"]):
                st.download_button(
                    label=f"📥 Download {file_obj.name}",
                    data=file_obj,
                    file_name=file_obj.name,
                    key=f"secure_download_btn_{idx}_{f_idx}",
                )
            else:
              st.markdown("*No files attached with this request.*")

            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
              if not req["is_responded"]:
                if st.button(
                    "✔️ Mark as Responded", key=f"resp_btn_{idx}"
                ):
                  st.session_state.client_requests[idx]["is_responded"] = True
                  st.rerun()
              else:
                if st.button("🔄 Mark as Unanswered", key=f"unresp_btn_{idx}"):
                  st.session_state.client_requests[idx]["is_responded"] = False
                  st.rerun()
            with c2:
              if st.button("🗑️ Delete Request", key=f"del_req_{idx}"):
                st.session_state.client_requests.pop(idx)
                st.rerun()

    elif admin_password:
      st.error("❌ Incorrect password. Access denied.")
    else:
      st.warning("⚠️ Please enter your password to view the requests.")
