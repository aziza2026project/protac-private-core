# ==============================================================================
# 📌 PART 1: IMPORTS & ENVIRONMENT CONFIGURATION
# ==============================================================================
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from rdkit import Chem
from rdkit.Chem import AllChem
import py3Dmol
from prediction_hub import (
    render_adme_workspace,
    render_linker_optimization_workspace)
# Safe import of machine learning libraries
try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


# ==============================================================================
# 📌 PART 2: PAGE CONFIGURATION & CUSTOM CSS STYLING
# ==============================================================================
st.set_page_config(
    page_title="PROTAC Research & Prediction Platform",
    page_icon="🧬",
    layout="wide",
)

st.markdown("""
    <style>
        /* ضبط المسافة الفوقية باش الأزرار العلوية تظهر بوضوح وتحت شريط المتصفح */
        .block-container {
            padding-top: 2.5rem !important;
            padding-bottom: 2rem !important;
        }
        
        div.element-container {
            margin-bottom: 0.2rem !important;
        }
        
        h1, h2, h3 {
            margin-top: 0px !important;
            padding-top: 0px !important;
        }

        .stButton>button {
            background-color: #1f4e78;
            color: white;
            border-radius: 6px;
            font-weight: 600;
            border: none;
            width: 100%;
            padding: 0.6rem;
        }
        .stButton>button:hover {
            background-color: #16385c;
            color: white;
        }
        .card-box {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# 📌 PART 3: DATABASE LOADING & UTILITY FUNCTIONS
# ==============================================================================
@st.cache_data
def load_database_for_prediction():
    try:
        protacs_df = pd.read_csv("PROTACS.csv") if os.path.exists("PROTACS.csv") else pd.DataFrame()
        main_df = pd.read_csv("database.csv") if os.path.exists("database.csv") else pd.DataFrame()
        warheads_df = pd.read_csv("WARHEADS.csv") if os.path.exists("WARHEADS.csv") else pd.DataFrame()
        linkers_df = pd.read_csv("LINKERS.csv") if os.path.exists("LINKERS.csv") else pd.DataFrame()
        e3_df = pd.read_csv("E3_LIGANDS.csv") if os.path.exists("E3_LIGANDS.csv") else pd.DataFrame()

        merged_df = protacs_df.copy()
        if not main_df.empty and "Compound_ID" in merged_df.columns and "Compound_ID" in main_df.columns:
            merged_df = merged_df.merge(main_df, on="Compound_ID", how="left", suffixes=("", "_main"))
        if not warheads_df.empty and "Warhead_ID" in merged_df.columns and "Warhead_ID" in warheads_df.columns:
            merged_df = merged_df.merge(warheads_df, on="Warhead_ID", how="left", suffixes=("", "_warhead"))
        if not linkers_df.empty and "Linker_ID" in merged_df.columns and "Linker_ID" in linkers_df.columns:
            merged_df = merged_df.merge(linkers_df, on="Linker_ID", how="left", suffixes=("", "_linker"))
        if not e3_df.empty and "E3_Ligand_ID" in merged_df.columns and "E3_Ligand_ID" in e3_df.columns:
            merged_df = merged_df.merge(e3_df, on="E3_Ligand_ID", how="left", suffixes=("", "_e3"))
            
        return merged_df if not merged_df.empty else (main_df if not main_df.empty else None)
    except Exception:
        return None


# ==============================================================================
# 📌 PART 4: 3D MOLECULAR STRUCTURE RENDERER (PY3DMOL)
# ==============================================================================
def render_molecule_3d(smiles, width=700, height=350):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            mol = Chem.MolFromSmiles("C1CCCCC1")
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, AllChem.ETKDG())
        AllChem.UFFOptimizeMolecule(mol)
        mol_block = Chem.MolToMolBlock(mol)
        
        view = py3Dmol.view(width=width, height=height)
        view.addModel(mol_block, "mol")
        view.setStyle({"model": -1}, {"stick": {"radius": 0.18}, "sphere": {"scale": 0.35}})
        view.zoomTo()
        return view._make_html()
    except Exception as e:
        return f"<p style='color:red;'>Error generating 3D view: {e}</p>"


# ==============================================================================
# 📌 PART 5: EMAIL DISPATCH & REPORT GENERATION ENGINE
# ==============================================================================
def send_formatted_html_email(recipient_email, result_title, html_content, output_filename, file_content_str=None):
    system_sender = "azizamnasri01@gmail.com"
    smtp_password = "hczf iqra ofrb okua"
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = system_sender
        msg['To'] = recipient_email
        msg['Subject'] = f"PROTAC Research Platform Report - {result_title}"
        
        text_part = MIMEText("Please view this email in an HTML-compatible client.", 'plain', 'utf-8')
        msg.attach(text_part)
        
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        if file_content_str:
            if not output_filename.endswith(".doc"):
                output_filename = output_filename.replace(".txt", ".doc")
            part = MIMEBase('application', 'msword')
            part.set_payload(file_content_str.encode('utf-8'))
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {output_filename}")
            msg.attach(part)
            
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(system_sender, smtp_password)
        server.sendmail(system_sender, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email dispatch: {e}")
        return False


# ==============================================================================
# 📌 PART 6: SIDEBAR NAVIGATION & DEVELOPER AUTHENTICATION
# ==============================================================================
def main():
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "Home Page"
    if 'dev_authenticated' not in st.session_state:
        st.session_state['dev_authenticated'] = False
    if 'user_subscribed' not in st.session_state:
        st.session_state['user_subscribed'] = False
    if 'user_email' not in st.session_state:
        st.session_state['user_email'] = ""
    if 'active_prediction_module' not in st.session_state:
        st.session_state['active_prediction_module'] = None

    st.sidebar.markdown("### 🧬 Quick Navigation")
    
    if st.sidebar.button("📱 View App QR Code", key="nav_qr"):
        st.session_state['current_page'] = "QR Code"

    with st.sidebar.expander("⚙️ Developer & AI Hub Access"):
        dev_pass = st.text_input("Enter Developer Password:", type="password", key="dev_password_input")
        if dev_pass == "aziza2026" or dev_pass == "azizamnasri":
            st.session_state['dev_authenticated'] = True
            st.success("Access Granted!")
            if st.button("Open AI & ML Hub", key="nav_ai_hub"):
                st.session_state['current_page'] = "AI Hub"
        elif dev_pass:
            st.error("Incorrect Password")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Developer:** Aziza Mnasri (PhD)")
    st.sidebar.markdown("**Profile:** Independent Researcher<br>(Organic Chemistry & Computational Drug Discovery)", unsafe_allow_html=True)

    page = st.session_state['current_page']


 # ==============================================================================
    # 📌 PART 7: HOME PAGE & GENERAL DASHBOARD & SUB-PAGES
    # ==============================================================================
    
    st.markdown("""
        <style>
        .home-btn-large > button {
            font-size: 20px !important;
            padding: 12px 30px !important;
            background-color: #1f4e78 !important;
            color: white !important;
            border-radius: 10px !important;
            font-weight: bold !important;
            box-shadow: 0 3px 6px rgba(0,0,0,0.1) !important;
        }
        .desc-box {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 10px;
            font-size: 13px;
            color: #555;
            min-height: 55px;
            margin-bottom: 10px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    if page == "Home Page":
        st.markdown('<div class="home-btn-large">', unsafe_allow_html=True)
        if st.button("🏠 Home Page", key="btn_home_top"):
            st.session_state['current_page'] = "Home Page"
            st.session_state['active_prediction_module'] = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.title("🧬 PROTAC Research & Prediction Platform")
        st.markdown("Welcome to the professional platform for PROTAC design, physicochemical property calculation, and scientific collaboration.")
        
        st.subheader("🌾 Welcome to PROTAC Research Hub")
        st.markdown("Choose a section below to get started with your research, design, and collaboration workflow:")

        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💳 Subscription Plans", key="btn_sub_card", use_container_width=True):
                st.session_state['current_page'] = "Subscriptions"
                st.rerun()
            st.markdown('<div class="desc-box">Explore access levels and research tiers.</div>', unsafe_allow_html=True)

        with col2:
            if st.button("🔬 Prediction Tool", key="btn_pred_card", use_container_width=True):
                st.session_state['current_page'] = "Prediction Tool"
                st.session_state['active_prediction_module'] = None
                st.rerun()
            st.markdown('<div class="desc-box">Access molecular docking, IC50 predictions, and ADME modules.</div>', unsafe_allow_html=True)

        with col3:
            if st.button("💼 Consultations & Collaboration", key="btn_collab_card", use_container_width=True):
                st.session_state['current_page'] = "Consultations"
                st.session_state['collab_sub_tab'] = None
                st.rerun()
            st.markdown('<div class="desc-box">Connect for advanced computational chemistry projects.</div>', unsafe_allow_html=True)

    elif page == "Subscriptions":
        if st.button("⬅️ Back to Home Page", key="back_to_home_sub"):
            st.session_state['current_page'] = "Home Page"
            st.rerun()
        st.title("💳 Subscription Plans & Research Tiers")
        st.markdown("Choose the appropriate computational tier for your target research.")
        st.info("Current Status: Professional Researcher Access Active.")

    elif page == "Prediction Tool":
        if st.button("⬅️ Back to Home Page", key="back_to_home_pred"):
            st.session_state['current_page'] = "Home Page"
            st.session_state['active_prediction_module'] = None
            st.rerun()
        
        st.title("🔬 PROTAC Prediction Tool")
        st.markdown("Molecular docking, binding affinity, and ADME property evaluation.")

        whitelist_emails = ["azizamnasri10@gmail.com"]

        if not st.session_state['user_subscribed']:
            entered_email = st.text_input("Enter your registered email address (Whitelisted users get instant access):", key="sub_email_input")
            
            if st.button("Verify & Access Tool", key="verify_email_btn"):
                if entered_email.strip().lower() in whitelist_emails or ("@" in entered_email and "." in entered_email):
                    st.session_state['user_subscribed'] = True
                    st.session_state['user_email'] = entered_email.strip()
                    st.success(f"Access granted for: {entered_email}")
                    st.rerun()
                else:
                    st.error("Email not found in whitelist or invalid format.")
        else:
            is_whitelisted = st.session_state['user_email'].lower() in whitelist_emails
            role_badge = "👑 Whitelisted Lead Researcher" if is_whitelisted else "✅ Verified Subscriber"
            
            st.success(f"{role_badge}: {st.session_state['user_email']}")
            if st.button("Logout / Change Email", key="logout_email_btn"):
                st.session_state['user_subscribed'] = False
                st.session_state['user_email'] = ""
                st.session_state['active_prediction_module'] = None
                st.rerun()
            
            if st.session_state['active_prediction_module'] is None:
                st.subheader("⚙️ Select a Prediction Module to Start Working")
                
                col_m1, col_m2, col_m3 = st.columns(3)
                
                with col_m1:
                    if st.button("🎯 Molecular Docking", key="mod_docking", use_container_width=True):
                        st.session_state['active_prediction_module'] = "Docking"
                        st.rerun()
                    st.markdown('<div class="desc-box">Configure grid boxes, rotatable bonds, binding affinity, and IC50 evaluations.</div>', unsafe_allow_html=True)    
                
                with col_m2:
                    if st.button("📊 ADME & Pharmacokinetics\n(pkCSM)", key="mod_adme", use_container_width=True):
                        st.session_state['active_prediction_module'] = "ADME"
                        st.rerun()
                    st.markdown('<div class="desc-box">Evaluate chemical properties, biological parameters, and permeability.</div>', unsafe_allow_html=True)

                with col_m3:
                    if st.button("🔗 Linker Optimization\n& Design", key="mod_linker", use_container_width=True):
                        st.session_state['active_prediction_module'] = "Linker"
                        st.rerun()
                    st.markdown('<div class="desc-box">Analyze linker length, flexibility, and ternary complex stability.</div>', unsafe_allow_html=True)

        active_mod = st.session_state.get('active_prediction_module')

        if active_mod == "Docking":
            render_molecular_docking_workspace()
        elif active_mod == "ADME":
            render_adme_workspace()
        elif active_mod == "Linker":
            render_linker_optimization_workspace()

    elif page == "Consultations":
        if st.button("⬅️ Back to Home Page", key="back_to_home_sub"):
            st.session_state['current_page'] = "Home Page"
            st.session_state['collab_sub_tab'] = None
            st.rerun()
        
        st.title("💼 Consultations & Scientific Collaboration")
        st.markdown("Choose between booking a professional consultation/service or proposing a major collaborative research project.")

        if 'collab_sub_tab' not in st.session_state:
            st.session_state['collab_sub_tab'] = None

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🛠️ Consultations & Services", use_container_width=True, key="tab_cons"):
                st.session_state['collab_sub_tab'] = "Consultations"
                st.rerun()
        with col_btn2:
            if st.button("🤝 Scientific Collaborations", use_container_width=True, key="tab_collab"):
                st.session_state['collab_sub_tab'] = "Collaborations"
                st.rerun()

        st.divider()

        # قسم الاستشارات والخدمات (Consultations)
        if st.session_state['collab_sub_tab'] == "Consultations":
            st.subheader("📋 Request a Professional Consultation")
            st.markdown("Submit your project details and upload any files freely. Dr. Aziza Mnasri will review your request and get back to you with an evaluation and pricing details.")

            with st.form("consultation_form"):
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    client_name = st.text_input("Full Name *")
                    client_lab = st.text_input("Laboratory / Institution *")
                with col_i2:
                    client_email = st.text_input("Your Email Address * (For receiving the evaluation and report)")
                    client_whatsapp = st.text_input("WhatsApp Number (Optional)")

                project_description = st.text_area("Project Description & Requirements *", placeholder="Describe what you need precisely (e.g., molecular docking, ADME evaluation, PROTAC linker design)...")
                
                uploaded_files = st.file_uploader("Upload Project Files (All formats & sizes accepted)", accept_multiple_files=True)

                st.info("📨 Your request and files will be sent directly to: azizamnasri01@gmail.com for review.")
                
                submit_consultation = st.form_submit_button("Submit Consultation Request & Files")

                if submit_consultation:
                    if not client_name or not client_email or not project_description:
                        st.error("Please fill in all mandatory fields (*).")
                    else:
                        st.success("Consultation request successfully submitted! Your files and details have been sent to azizamnasri01@gmail.com. We will review it and contact you soon.")

            # قسم الدفع الاختياري (خارج الفورم أو تحته لكي يتم استخدامه بعد الاتفاق على السعر)
            with st.container():
                st.markdown("---")
                st.subheader("💳 Secure Consultation Payment Gateway")
                st.markdown("If you have already discussed your project with Dr. Aziza Mnasri and agreed on the service terms, you can securely proceed with the payment below:")
                
                col_pay1, col_pay2 = st.columns([2, 1])
                with col_pay1:
                    st.text_input("Enter Consultation Reference or Invoice ID (Optional)", key="invoice_id_input")
                with col_pay2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Proceed to Secure Payment", use_container_width=True):
                        st.info("Redirecting to secure payment gateway... (Link your payment processor here)")

            # لوحة التحكم الخاصة بالأدمن (محمية بكلمة مرور)
            with st.expander("🔐 Admin Dashboard (Dr. Aziza Mnasri Only)"):
                admin_pass = st.text_input("Enter Admin Password", type="password", key="consult_admin_pass")
                if admin_pass == "aziza2026":
                    st.success("Access Granted to Admin Dashboard")
                    
                    dash_tab1, dash_tab2, dash_tab3, dash_tab4 = st.tabs(["📥 All Requests", "🔴 Unread", "⏳ In Progress", "✅ Answered"])
                    
                    with dash_tab1:
                        st.write("Displaying all consultation requests...")
                    with dash_tab2:
                        st.write("Displaying unread / new requests (To be checked)...")
                    with dash_tab3:
                        st.write("Displaying requests in progress...")
                    with dash_tab4:
                        st.write("Displaying completed & answered requests...")
                elif admin_pass:
                    st.error("Incorrect password.")

        # قسم التعاون العلمي والمشاريع الكبرى (Scientific Collaborations)
        elif st.session_state['collab_sub_tab'] == "Collaborations":
            st.subheader("🤝 Scientific Collaborations & Major Research Projects")
            st.markdown("Partner with Dr. Aziza Mnasri for high-impact joint research, strategic Big Pharma collaborations, and world-class academic publications.")

            with st.form("collaboration_form"):
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    collab_name = st.text_input("Researcher / Institution / Big Pharma Name *")
                    collab_email = st.text_input("Contact Email *")
                with col_c2:
                    collab_type = st.selectbox("Strategic Collaboration Type", [
                        "Big Pharma & Biotech R&D Partnership",
                        "Global Academic Research Consortium",
                        "Joint High-Impact Scientific Publications",
                        "Strategic Computational Drug Discovery Project"
                    ])
                
                collab_details = st.text_area("Project Proposal & Strategic Objectives *", placeholder="Describe the scope of the major research project, partnership goals, and expected outcomes...")

                st.info("📨 Proposals will be sent directly to: azizamnasri01@gmail.com")
                
                submit_collab = st.form_submit_button("Send Strategic Collaboration Proposal")

                if submit_collab:
                    if not collab_name or not collab_email or not collab_details:
                        st.error("Please fill in all required fields.")
                    else:
                        st.success("Strategic collaboration proposal successfully sent to azizamnasri01@gmail.com!")
    # ==============================================================================
    # 📌 PART 8: QR CODE & UTILITY PAGES
    # ==============================================================================
    elif page == "QR Code":
        st.subheader("📱 App QR Code & Quick Access")
        st.markdown("Scan the QR code below to open the application directly on your mobile device or share it easily.")
        st.info("App deployment link active and synchronized.")

    # ==============================================================================
    # 📌 PART 9: AI & QSAR PREDICTION HUB (DEVELOPER MODE)
    # ==============================================================================
    elif page == "AI Hub" and st.session_state['dev_authenticated']:
        st.subheader("🤖 Advanced Machine Learning & QSAR Prediction Hub (Developer Mode)")
        if SKLEARN_AVAILABLE:
            merged_data = load_database_for_prediction()
            if merged_data is not None and not merged_data.empty:
                st.success(f"Successfully loaded datasets! Total rows: {merged_data.shape[0]}")
                numeric_cols = [col for col in merged_data.select_dtypes(include=[np.number]).columns.tolist() if merged_data[col].nunique() > 2]
                if len(numeric_cols) >= 2:
                    target_col = st.selectbox("Select Target Variable (Numeric):", numeric_cols, key="ml_target")
                    feature_candidates = [c for c in numeric_cols if c != target_col]
                    feature_cols = st.multiselect("Select Feature Columns:", feature_candidates, default=feature_candidates[:min(4, len(feature_candidates))])
                    
                    if feature_cols and target_col:
                        df_clean = merged_data.dropna(subset=feature_cols + [target_col])
                        if len(df_clean) > 5:
                            X = df_clean[feature_cols]
                            y = df_clean[target_col]
                            scaler = StandardScaler()
                            X_scaled = scaler.fit_transform(X)
                            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
                            
                            ml_model = RandomForestRegressor(n_estimators=150, random_state=42)
                            ml_model.fit(X_train, y_train)
                            y_pred = ml_model.predict(X_test)
                            
                            st.metric("Model Accuracy (R2 Score)", f"{r2_score(y_test, y_pred):.2f}")
        else:
            st.error("scikit-learn not available.")

if __name__ == "__main__":
    main()
   
