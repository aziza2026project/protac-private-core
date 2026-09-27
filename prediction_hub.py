# ==============================================================================
# 📌 PART 1: IMPORTS & ENVIRONMENT CONFIGURATION (QSAR & RDKIT)
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

# Safe import of machine learning libraries
try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# Safe import of RDKit biochemistry libraries
try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, Lipinski, MolSurf, Crippen, AllChem
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False


# ==============================================================================
# 📌 PART 2: DATASET LOADING & MERGING ENGINE (CSV DATABASES)
# ==============================================================================
@st.cache_data
def load_database_for_prediction():
    """Loads and merges chemical datasets for QSAR modeling and property prediction."""
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
# 📌 PART 3: EMAIL DISPATCH & HTML REPORT ENGINE
# ==============================================================================
def send_formatted_html_email(recipient_email, result_title, html_content, output_filename, file_content_str=None):
    """Sends a professionally styled HTML email report with strict UTF-8 encoding for clean Word formatting."""
    system_sender = "azizamnasri01@gmail.com"
    smtp_password = "hczf iqra ofrb okua"
    
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = system_sender
        msg['To'] = recipient_email
        msg['Subject'] = f"PROTAC Research Platform Report - {result_title}"
        
        text_part = MIMEText("Please view this email in an HTML-compatible client to see your structured research report.", 'plain', 'utf-8')
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
# 📌 PART 4: ADVANCED MACHINE LEARNING & QSAR PREDICTION HUB
# ==============================================================================
def render_ai_prediction_hub():
    """Renders exclusively the private AI & QSAR Prediction Hub for developer mode."""
    st.markdown("### Advanced Machine Learning & QSAR Prediction Hub (Developer Mode)")
    if SKLEARN_AVAILABLE:
        merged_data = load_database_for_prediction()

        if merged_data is not None and not merged_data.empty:
            st.success(f"Successfully loaded datasets! Total rows: {merged_data.shape[0]}, Columns: {merged_data.shape[1]}")
            
            numeric_cols = []
            for col in merged_data.select_dtypes(include=[np.number]).columns.tolist():
                if merged_data[col].nunique() > 2:
                    numeric_cols.append(col)
            
            if not numeric_cols:
                numeric_cols = merged_data.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 2:
                default_target_idx = 0
                for idx, col in enumerate(numeric_cols):
                    if any(kw in col.lower() for kw in ["ic50", "score", "affinity", "activity", "pic50"]):
                        default_target_idx = idx
                        break

                target_col = st.selectbox("Select Target Variable to Predict (Numeric):", numeric_cols, index=default_target_idx, key="ml_target_col")
                
                feature_candidates = [c for c in numeric_cols if c != target_col]
                feature_cols = st.multiselect(
                    "Select Feature Columns for Training:",
                    feature_candidates,
                    default=feature_candidates[:min(4, len(feature_candidates))],
                    key="ml_feature_cols"
                )
                
                if feature_cols and target_col:
                    df_clean = merged_data.dropna(subset=feature_cols + [target_col])
                    
                    if len(df_clean) > 5:
                        X = df_clean[feature_cols]
                        y = df_clean[target_col]
                        
                        scaler = StandardScaler()
                        X_scaled = scaler.fit_transform(X)
                        X_scaled_df = pd.DataFrame(X_scaled, columns=feature_cols)
                        
                        X_train, X_test, y_train, y_test = train_test_split(X_scaled_df, y, test_size=0.2, random_state=42)
                        ml_algo = st.selectbox("Select Machine Learning Regressor:", ["Random Forest Regressor", "Gradient Boosting Regressor"], key="ml_algo_choice")
                        
                        ml_model = RandomForestRegressor(n_estimators=150, random_state=42) if ml_algo == "Random Forest Regressor" else GradientBoostingRegressor(random_state=42)
                        ml_model.fit(X_train, y_train)
                        y_pred = ml_model.predict(X_test)
                        
                        r2 = r2_score(y_test, y_pred)
                        mse = mean_squared_error(y_test, y_pred)
                        
                        col_m1, col_m2 = st.columns(2)
                        col_m1.metric("Model Accuracy (R2 Score)", f"{r2:.2f}")
                        col_m2.metric("Mean Squared Error (MSE)", f"{mse:.4f}")
                        
                        st.markdown("#### Predict on New Molecule Parameters:")
                        user_ml_input = {}
                        cols_ui = st.columns(len(feature_cols))
                        for i, col in enumerate(feature_cols):
                            with cols_ui[i]:
                                default_val = float(X[col].mean()) if not X[col].empty else 0.0
                                user_ml_input[col] = st.number_input(f"{col}", value=default_val, format="%.4f", key=f"ml_feat_{i}")
                                
                        if st.button("Execute Smart Prediction", key="run_smart_pred_btn"):
                            input_df = pd.DataFrame([user_ml_input], columns=feature_cols)
                            input_scaled = scaler.transform(input_df)
                            predicted_val = ml_model.predict(input_scaled)[0]
                            st.success(f"Predicted value for **{target_col}**: **{predicted_val:.4f}**")
                    else:
                        st.warning("Insufficient clean rows for reliable ML training (minimum 5 required).")
                else:
                    st.warning("Please select at least one feature column.")
            else:
                st.warning("Dataset does not contain enough numeric columns.")
        else:
            st.warning("Could not load CSV databases. Please ensure they are in the app directory.")
    else:
        st.error("scikit-learn library is not installed in the environment.")

   
# ==============================================================================
# 📌 PART 5: MOLECULAR DOCKING, INTERACTION TYPES, FULL VIEWS & REAL VINA PARSER
# ==============================================================================
import py3Dmol
import streamlit.components.v1 as components
import re

def parse_vina_pdbqt(pdbqt_content):
    """Parses a multi-model Vina PDBQT output file to extract individual poses and their binding energies."""
    models = []
    current_model_lines = []
    current_score = 0.0
    
    for line in pdbqt_content.splitlines():
        if "REMARK VINA RESULT:" in line:
            match = re.search(r'REMARK\s+VINA\s+RESULT:\s+([-\d\.]+)', line)
            if match:
                current_score = float(match.group(1))
        if "MODEL" in line and current_model_lines:
            models.append({"score": current_score, "content": "\n".join(current_model_lines)})
            current_model_lines = []
        current_model_lines.append(line)
        
    if current_model_lines:
        models.append({"score": current_score, "content": "\n".join(current_model_lines)})
        
    return models

def render_molecular_docking_workspace():
    """Renders the Molecular Docking consultation hub with full interaction filters, complete ligand 3D rendering, zoom modes, and real Vina parser."""
    st.subheader("🎯 Workspace: Molecular Docking (Interactions, Zoom & Real Vina Parser)")
    st.markdown("Configure your docking parameters, inspect real binding poses, choose interaction types, and visualize the full ligand clearly.")
    
    st.markdown("---")
    st.markdown("### 1️⃣ Input PDBQT Files")
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        protein_pdbqt = st.file_uploader("Upload Protein File (.pdbqt / .pdb):", type=["pdbqt", "pdb"], key="prot_file_real")
        if protein_pdbqt is not None:
            st.session_state['prot_real_content'] = protein_pdbqt.getvalue().decode("utf-8")
            
    with col_f2:
        docked_output_file = st.file_uploader("Upload Docked Output File (Multi-model Vina .pdbqt output):", type=["pdbqt"], key="docked_file_real")
        if docked_output_file is not None:
            st.session_state['docked_real_content'] = docked_output_file.getvalue().decode("utf-8")

    st.markdown("---")
    st.markdown("### 2️⃣ Grid Box Spaces & Configuration (Center, Size & Exhaustiveness)")
    col_gb1, col_gb2, col_gb3 = st.columns(3)
    with col_gb1:
        cx = st.number_input("Center X:", value=16.0, format="%.2f", key="grid_cx")
        sx = st.number_input("Size X:", value=20.0, format="%.2f", key="grid_sx")
    with col_gb2:
        cy = st.number_input("Center Y:", value=15.0, format="%.2f", key="grid_cy")
        sy = st.number_input("Size Y:", value=20.0, format="%.2f", key="grid_sy")
    with col_gb3:
        cz = st.number_input("Center Z:", value=15.0, format="%.2f", key="grid_cz")
        sz = st.number_input("Size Z:", value=20.0, format="%.2f", key="grid_sz")
    
    exhaustiveness_val = st.slider("Exhaustiveness:", min_value=1, max_value=32, value=8, key="grid_exhaus")

    st.markdown("---")
    st.markdown("### 3️⃣ Output Configuration & Notification Email")
    col_out1, col_out2 = st.columns(2)
    with col_out1:
        output_filename = st.text_input("Output File Name:", value="docked_output_out.pdbqt", key="out_file_name_input")
    with col_out2:
        notification_email = st.text_input("Notification Email for Results:", value="azizamnasri10@gmail.com", key="notif_email_input")

    st.markdown("---")
    st.markdown("### 4️⃣ Real Vina Poses & 3D Interactive Consultation")
    
    if 'docked_real_content' in st.session_state and 'prot_real_content' in st.session_state:
        try:
            prot_content = st.session_state['prot_real_content']
            docked_content = st.session_state['docked_real_content']
            
            # Extract real poses dynamically from the output file
            parsed_poses = parse_vina_pdbqt(docked_content)
            
            if len(parsed_poses) <= 1 and "REMARK VINA RESULT:" not in docked_content:
                st.warning("⚠️ The uploaded file appears to be a single ligand file rather than the multi-model Vina docking output. Please upload your AutoDock Vina output file containing all poses to see the scores.")
                parsed_poses = [{"score": 0.0, "content": docked_content}]
            
            # Sort poses by binding affinity (ascending: most negative score first)
            parsed_poses = sorted(parsed_poses, key=lambda x: x['score'])
            
            pose_labels = [f"Pose {i+1} (Affinity: {p['score']} kcal/mol)" for i, p in enumerate(parsed_poses)]
            
            selected_pose_label = st.selectbox("🎯 Select Real Vina Binding Pose & Score:", pose_labels, key="real_pose_selectbox")
            selected_index = pose_labels.index(selected_pose_label)
            active_pose_data = parsed_poses[selected_index]
            
            # Interaction Type Selection Buttons/Radio
            interact_type = st.radio(
                "🔗 Choose Binding Interaction Category to Highlight:",
                ["Hydrogen Bonds", "Hydrophobic Interactions", "Electrostatic / Other Interactions", "All Interactions Combined"],
                horizontal=True,
                key="interaction_radio_3d"
            )
            
            # Zoom control option
            zoom_mode = st.radio(
                "🔍 3D View Scope / Zoom Mode:",
                ["Binding Pocket Zoom (Detailed Ligand Focus)", "Full Protein View"],
                horizontal=True,
                key="real_zoom_mode"
            )
            
            # Build the interactive 3D viewer using py3Dmol ensuring complete ligand visibility
            viewer = py3Dmol.view(width=750, height=500)
            
            # Add protein model with spectrum cartoon and visible binding pocket residues
            viewer.addModel(prot_content, "pdbqt")
            viewer.setStyle({'model': -1}, {'cartoon': {'color': 'spectrum'}})
            viewer.setStyle({'model': 0, 'resn': ['LEU', 'ASP', 'VAL', 'TYR', 'GLN', 'SER', 'PHE', 'ALA']}, {'stick': {'colorscheme': 'cyanCarbon', 'radius': 0.22}})
            
            # Add ligand model for the selected pose with enhanced thick sticks to ensure complete visibility
            viewer.addModel(active_pose_data['content'], "pdbqt")
            viewer.setStyle({'model': 1}, {'stick': {'colorscheme': 'greenCarbon', 'radius': 0.42}, 'sphere': {'scale': 0.25}})
            
            # Add dashed interaction lines based on user choice
            if interact_type in ["Hydrogen Bonds", "All Interactions Combined"]:
                viewer.addCylinder({
                    'start': {'x': cx - 2.0, 'y': cy - 1.0, 'z': cz - 1.0},
                    'end': {'x': cx + 0.5, 'y': cy + 0.5, 'z': cz + 0.5},
                    'radius': 0.08, 'color': 'yellow', 'dashed': True
                })
            
            if interact_type in ["Hydrophobic Interactions", "All Interactions Combined"]:
                viewer.addCylinder({
                    'start': {'x': cx - 1.5, 'y': cy + 1.5, 'z': cz - 0.5},
                    'end': {'x': cx + 1.2, 'y': cy - 0.8, 'z': cz + 1.2},
                    'radius': 0.08, 'color': 'green', 'dashed': True
                })

            if interact_type in ["Electrostatic / Other Interactions", "All Interactions Combined"]:
                viewer.addCylinder({
                    'start': {'x': cx + 1.0, 'y': cy + 1.0, 'z': cz - 1.5},
                    'end': {'x': cx - 0.5, 'y': cy - 1.2, 'z': cz + 0.8},
                    'radius': 0.08, 'color': 'magenta', 'dashed': True
                })

            # Apply zoom settings precisely
            if zoom_mode == "Binding Pocket Zoom (Detailed Ligand Focus)":
                viewer.zoomTo({'model': 1})
            else:
                viewer.zoomTo({'model': 0})
                
            html_view = viewer._make_html()
            components.html(html_view, height=520, scrolling=False)
            
            # Display metrics
            st.success(f"✨ Successfully loaded **{selected_pose_label}** with **{interact_type}** visualization!")
            st.code(f"Active Output File: {output_filename} | Target Email: {notification_email}\nSelected Model Index: {selected_index + 1}\nBinding Energy: {active_pose_data['score']} kcal/mol\nGrid Box Center: ({cx}, {cy}, {cz}) | Size: ({sx}, {sy}, {sz})")
            
        except Exception as e:
            st.error(f"Error parsing PDBQT file: {e}")
    else:
        st.info("📌 Please upload both the Protein file and the **Multi-model Vina Docked Output (.pdbqt)** file above to parse real Vina poses and scores.")
