import datetime
import pandas as pd
import streamlit as st


def render_services_section():
  st.subheader("🤝 Consultations & Scientific Collaboration")

  # تهيئة صندوق الوارد في الذاكرة لضمان حفظ الطلبات
  if "client_requests" not in st.session_state:
    st.session_state.client_requests = []

  # تهيئة حالة الفلتر في الذاكرة إذا لم تكن موجودة
  if "admin_filter" not in st.session_state:
    st.session_state.admin_filter = "All"

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

      # السماح بجميع أنواع الملفات ورفع ملفات متعددة
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
              "files": uploaded_files,
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
        # حساب الأعداد بحسب الحالات
        total = len(st.session_state.client_requests)
        unread = sum(
            1
            for r in st.session_state.client_requests
            if not r.get("is_read", False)
        )
        responded = sum(
            1
            for r in st.session_state.client_requests
            if r.get("is_responded", False)
        )

        st.markdown("---")
        st.markdown(
            "📌 **Filter Requests:** Click below to filter by status:"
        )

        # أزرار تفاعلية لتصفية الطلبات مع أيقونات مميزة
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
          if st.button(f"📥 All Requests ({total})"):
            st.session_state.admin_filter = "All"
            st.rerun()
        with col_f2:
          if st.button(f"🆕 Unread ({unread})"):
            st.session_state.admin_filter = "Unread"
            st.rerun()
        with col_f3:
          if st.button(f"✅ Responded ({responded})"):
            st.session_state.admin_filter = "Responded"
            st.rerun()

        st.markdown(
            f"current Active Filter: **{st.session_state.admin_filter}**"
        )
        st.markdown("---")

        # ترتيب الطلبات من الأحدث إلى الأقدم مع الاحتفاظ بالـ Index الأصلي
        indexed_requests = list(enumerate(st.session_state.client_requests))[
            ::-1
        ]

        # تصفية القائمة حسب اختيار المستخدم
        filtered_requests = []
        for idx, req in indexed_requests:
          is_resp = req.get("is_responded", False)
          is_rd = req.get("is_read", False)

          if st.session_state.admin_filter == "Unread" and (
              is_rd or is_resp
          ):
            continue
          if st.session_state.admin_filter == "Responded" and not is_resp:
            continue
          filtered_requests.append((idx, req))

        if not filtered_requests:
          st.info(
              f"📭 No requests found under filter:"
              f" {st.session_state.admin_filter}."
          )
        else:
          for idx, req in filtered_requests:
            req_name = req.get("name", "Unknown")
            req_email = req.get("email", "No Email")
            req_time = req.get("timestamp", "Unknown Time")
            req_details = req.get("details", "No details provided.")
            is_resp = req.get("is_responded", False)
            is_rd = req.get("is_read", False)

            # تمييز الأيقونات بحسب الحالة بدقة
            if is_resp:
              status_icon = "✅ [Responded]"
            elif not is_rd:
              status_icon = "🆕 [Unread]"
            else:
              status_icon = "👁️ [Read / Unanswered]"

            title_str = (
                f"{status_icon} Request #{idx+1} | {req_name} ({req_email}) —"
                f" [{req_time}]"
            )

            with st.expander(title_str):
              # تحديث حالة القراءة تلقائياً عند فتح الطلب
              if not req.get("is_read", False):
                st.session_state.client_requests[idx]["is_read"] = True

              st.markdown(f"**🕒 Time:** {req_time}")
              st.markdown(f"**👤 Client Name:** {req_name}")
              st.markdown(f"**📧 Email:** {req_email}")
              st.markdown(f"**📝 Project Details:**\n{req_details}")

              files_list = req.get("files", [])
              if files_list and len(files_list) > 0:
                st.markdown(f"**📎 Attached Files ({len(files_list)} files):**")
                for f_idx, file_obj in enumerate(files_list):
                  if file_obj is not None:
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
                if not is_resp:
                  if st.button(
                      "✔️ Mark as Responded", key=f"resp_btn_{idx}"
                  ):
                    st.session_state.client_requests[idx]["is_responded"] = True
                    st.rerun()
                else:
                  if st.button(
                      "🔄 Mark as Unanswered", key=f"unresp_btn_{idx}"
                  ):
                    st.session_state.client_requests[idx]["is_responded"] = (
                        False
                    )
                    st.rerun()
              with c2:
                if st.button("🗑️ Delete Request", key=f"del_req_{idx}"):
                  st.session_state.client_requests.pop(idx)
                  st.rerun()

    elif admin_password:
      st.error("❌ Incorrect password. Access denied.")
    else:
      st.warning("⚠️ Please enter your password to view the requests.")
