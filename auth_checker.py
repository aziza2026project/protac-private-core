import streamlit as st

def check_email_access():
    st.subheader("🔐 Access Control & Verification")
    st.markdown("Please enter your email address to access the prediction tools:")
    
    whitelist = ["azizamnasri10@gmail.com", "azizamnasri01@gmail.com", "admin@protac.com"]
    blacklist = ["blocked_user@example.com", "spam@test.com"]
    
    user_email = st.text_input("📧 Email Address:", placeholder="example@domain.com", key="auth_email_input")
    
    if st.button("Verify Access", key="verify_btn"):
        if not user_email:
            st.error("Please enter a valid email address.")
            return False
            
        user_email = user_email.strip().lower()
        
        if user_email in [b.lower() for b in blacklist]:
            st.error("❌ Access denied. This email address is blacklisted.")
            return False
            
        elif user_email in [w.lower() for w in whitelist]:
            st.success("✅ Welcome! Your email is whitelisted. You can proceed to the prediction tool.")
            st.session_state['authenticated'] = True
            st.session_state['user_email'] = user_email
            return True
            
        else:
            st.warning("⚠️ Your email is not registered in the free tier. Please visit the Subscription section to activate your account.")
            st.session_state['authenticated'] = False
            return False
            
    return st.session_state.get('authenticated', False)
