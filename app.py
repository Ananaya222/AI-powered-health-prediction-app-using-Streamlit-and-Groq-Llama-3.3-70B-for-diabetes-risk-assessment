import streamlit as st
import pandas as pd
from datetime import datetime
import re
import time
from database import init_db, add_patient, get_all_patients, update_patient, delete_patient, get_patient_by_id
from model import predict_risk

# Initialize database
init_db()

# Page configuration
st.set_page_config(page_title="MIRA Health Predictor", page_icon="🏥", layout="wide")

# Title
st.title("🏥 MIRA - Medical Intelligence Robotic Automation")
st.subheader("AI-Powered Health Prediction & Diabetes Risk Assessment")
st.caption("Powered by Groq Llama 3.3 70B")

# Sidebar navigation
menu = st.sidebar.radio("Menu", ["➕ Add New Patient", "📋 View/Manage Patients"])

# --- Helper functions ---
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_dob(dob):
    return dob <= datetime.now().date()

# --- Add Patient Section ---
if menu == "➕ Add New Patient":
    st.header("Enter Patient Details")
    
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *")
            dob = st.date_input("Date of Birth *", max_value=datetime.now())
            email = st.text_input("Email Address *")
        
        with col2:
            glucose = st.number_input("Glucose (mg/dL) *", min_value=0.0, step=0.1)
            haemoglobin = st.number_input("Haemoglobin (g/dL) *", min_value=0.0, step=0.1)
            cholesterol = st.number_input("Cholesterol (mg/dL) *", min_value=0.0, step=0.1)
        
        submitted = st.form_submit_button("🔍 Predict & Save Patient")
        
        if submitted:
            errors = []
            if not full_name:
                errors.append("Full name required")
            if not is_valid_dob(dob):
                errors.append("Date of Birth cannot be in the future")
            if not is_valid_email(email):
                errors.append("Invalid email format")
            if glucose <= 0:
                errors.append("Glucose must be positive")
            if haemoglobin <= 0:
                errors.append("Haemoglobin must be positive")
            if cholesterol <= 0:
                errors.append("Cholesterol must be positive")
            
            if errors:
                for err in errors:
                    st.error(err)
            else:
                with st.spinner("🤖 AI is analyzing health data via Groq..."):
                    remarks = predict_risk(glucose, haemoglobin, cholesterol)
                
                add_patient(full_name, dob.strftime("%Y-%m-%d"), email,
                           glucose, haemoglobin, cholesterol, remarks)
                st.success(f"✅ Patient {full_name} added successfully!")
                st.info(f"🧠 **AI Assessment:**\n{remarks}")

# --- View/Manage Patients Section ---
elif menu == "📋 View/Manage Patients":
    st.header("Patient Records")
    
    patients = get_all_patients()
    
    if not patients:
        st.info("No patients found. Go to 'Add New Patient' to create records.")
    else:
        df = pd.DataFrame(patients)
        display_df = df[['id', 'full_name', 'date_of_birth', 'email', 'glucose', 'haemoglobin', 'cholesterol', 'remarks']]
        display_df.columns = ['ID', 'Name', 'DOB', 'Email', 'Glucose', 'Hb', 'Chol', 'AI Remarks']
        st.dataframe(display_df, use_container_width=True)
        
        st.subheader("✏️ Edit or Delete Record")
        patient_ids = [p['id'] for p in patients]
        selected_id = st.selectbox("Select Patient ID", patient_ids)
        
        patient = get_patient_by_id(selected_id)
        if patient:
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Name", patient['full_name'])
                # Convert date string to date object
                dob_obj = datetime.strptime(patient['date_of_birth'], "%Y-%m-%d").date()
                new_dob = st.date_input("DOB", dob_obj)
                new_email = st.text_input("Email", patient['email'])
            
            with col2:
                new_glucose = st.number_input("Glucose", value=float(patient['glucose']), step=0.1)
                new_haemoglobin = st.number_input("Haemoglobin", value=float(patient['haemoglobin']), step=0.1)
                new_cholesterol = st.number_input("Cholesterol", value=float(patient['cholesterol']), step=0.1)
            
            col_up, col_del = st.columns(2)
            
            with col_up:
                if st.button("🔄 Update & Re-predict"):
                    if not new_name or not is_valid_email(new_email):
                        st.error("Invalid name or email")
                    elif new_glucose <= 0 or new_haemoglobin <= 0 or new_cholesterol <= 0:
                        st.error("Values must be positive")
                    else:
                        with st.spinner("AI re‑evaluating..."):
                            new_remarks = predict_risk(new_glucose, new_haemoglobin, new_cholesterol)
                        
                        # Show the new AI remark immediately
                        st.success("✅ Patient updated!")
                        st.info(f"🧠 **New AI Assessment:**\n{new_remarks}")
                        
                        # Update database
                        update_patient(selected_id, new_name, new_dob.strftime("%Y-%m-%d"), new_email,
                                      new_glucose, new_haemoglobin, new_cholesterol, new_remarks)
                        
                        # Pause briefly so user can read the message, then refresh
                        time.sleep(3)
                        st.rerun()
            
            with col_del:
                if st.button("🗑️ Delete Patient", type="primary"):
                    delete_patient(selected_id)
                    st.warning(f"Patient {selected_id} deleted.")
                    time.sleep(1.5)
                    st.rerun()
