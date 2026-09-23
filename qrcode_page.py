import io
import qrcode
import streamlit as st


def render_qrcode_page():
  st.markdown("## 📱 Web App QR Code & Access Hub")
  st.markdown(
      "هذه الصفحة مخصصة لتوليد وتحميل رمز الاستجابة السريعة (QR Code) الخاص"
      " بمنصتك للبحوث العلمية، البوسترات، والمؤتمرات."
  )

  col1, col2 = st.columns([1, 1])

  with col1:
    st.markdown("### 📌 تفاصيل الرابط المباشر:")
    app_url = "https://protac-app-core.streamlit.app"
    st.info(f"🔗 **رابط المنصة:** `{app_url}`")
    st.markdown(
        "يمكنك مشاركة هذا الرابط مباشرة في قسم *Availability of Data and"
        " Software* في مقالك العلمي."
    )

    # توليد الـ QR Code برمجياً
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(app_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # حفظ الصورة في الذاكرة المؤقتة
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 تحميل صورة QR Code (PNG عالي الجودة)",
        data=byte_im,
        file_name="PROTAC_Platform_QRCode.png",
        mime="image/png",
    )

  with col2:
    st.markdown("### 👁️ معاينة الرمز المباشر:")
    # عرض الصورة في الواجهة بحجم مناسب
    st.image(byte_im, width=240)

  st.markdown("---")
  st.markdown("### 💡 نصائح لاحترافية البوستر والمقال العلمي:")
  st.markdown(
      "* **في البوستر (Poster):** ضع الـ QR Code في الزاوية مع عبارة مثل *"
      "Scan to test the platform live"*. يتيح للمحكمين تجربة المنصة فوراً."
  )
  st.markdown(
      "* **في المقال (Paper):** أضف الرابط النصي صريحاً، ويمكنك إرفاق الـ QR"
      " Code في الـ Supplementary Materials."
  )
