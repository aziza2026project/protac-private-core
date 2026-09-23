import streamlit as st

def render_services_section():
    st.subheader("🤝 Consultations & Scientific Collaboration")
    
    tab1, tab2 = st.tabs(["💡 Custom Consultation", "🔬 Research Collaboration"])
    
    with tab1:
        st.markdown("### Request a Custom Research Report")
        st.markdown("Need a deep-dive analysis, custom molecular docking, or tailored PROTAC design? You can contact me directly:")
        st.info("📧 **Direct Contact Email:** aziza.mnasri@example.com")
        st.markdown("Feel free to send an email with your project details, objectives, and timeline, and I will get back to you promptly.")
                
    with tab2:
        st.markdown("### Academic & Industrial Partnership")
        st.markdown("Interested in co-authoring papers, joint research grants, or technological integration? Let's connect.")
        st.success("🤝 **For Collaboration Inquiries:** azizamnasri10gmail.com")
        st.markdown("Send your institution name, proposal, or collaboration idea directly to my email.")
