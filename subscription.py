import pandas as pd
import streamlit as st


def render_subscription_section():
  st.subheader("💳 Subscription & Pricing Plans")
  st.markdown(
      "Choose the appropriate plan for your research needs and unlock advanced"
      " in-silico computational tools:"
  )

  # جدول الأسعار والخطط المتاحة
  pricing_data = [
      {
          "Tier": "Academic Tier (Monthly)",
          "Price": "$29 / month",
          "Target Audience": "Students, Researchers, Academic Labs",
          "Features": (
              "Full Access to Docking, ADME (pkCSM), and RDKit Descriptors"
          ),
      },
      {
          "Tier": "Academic Tier (Annual)",
          "Price": "$250 / year",
          "Target Audience": "Long-term Research Projects",
          "Features": "All Academic Features + Priority Queue + Save Reports",
      },
      {
          "Tier": "Enterprise / Lab Tier",
          "Price": "Custom Pricing",
          "Target Audience": "Pharmaceutical Companies & Research Institutes",
          "Features": "Dedicated Server, Custom Database Integration, API Access",
      },
  ]

  pricing_df = pd.DataFrame(pricing_data)
  st.table(pricing_df)

  st.markdown("---")
  st.markdown("### 🚀 Proceed to Checkout")

  selected_tier = st.selectbox(
      "Select Subscription Tier:",
      [
          "Academic Tier (Monthly) - $29",
          "Academic Tier (Annual) - $250",
          "Enterprise / Lab Tier - Custom",
      ],
      key="sub_tier_select",
  )

  user_email = st.text_input(
      "Enter your institutional or personal email for subscription:",
      placeholder="name@university.edu",
      key="sub_email_input",
  )

  if st.button("🔒 Proceed to Secure Payment", key="checkout_btn"):
    if user_email:
      st.success(
          f"✅ Registration initiated for `{user_email}` with package:"
          f" **{selected_tier}**."
      )

      # إرشادات الدفع المؤقتة والمتوافقة مع الوضع في تونس (Payoneer / التحويل)
      st.info(
          "💡 **Payment Instructions:** \n"
          "Since automated international gateway integration is currently being"
          " configured for your region, please complete your payment via our"
          " secure link (Payoneer / Direct Wire Transfer) or contact support"
          " directly to activate your account instantly."
      )

      st.markdown(
          "[🔗 Click here to complete secure payment via Payoneer / Direct"
          " Transfer](https://payoneer.com)",
          unsafe_allow_html=True,
      )
    else:
      st.error("Please enter a valid email address to proceed.")
