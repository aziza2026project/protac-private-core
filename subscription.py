import streamlit as st

def render_subscription_section():
    st.subheader("💳 Subscription & Pricing Plans")
    st.markdown("Choose a plan or enter your email to upgrade your account and access advanced prediction tools:")
    
    plan = st.selectbox("Select Subscription Tier:", ["Academic Tier (Monthly)", "Enterprise Tier (Annual)", "Custom Pay-Per-Analysis"])
    user_email = st.text_input("📧 Enter your email for subscription:", placeholder="your.email@domain.com", key="sub_email_input")
    
    if st.button("Proceed to Secure Payment", key="pay_btn"):
        if user_email:
            st.success(f"Redirecting to payment gateway for {user_email} ({plan})...")
            st.info("🔒 Secure payment integration (Stripe/PayPal) will be connected here.")
        else:
            st.error("Please enter your email address first.")
