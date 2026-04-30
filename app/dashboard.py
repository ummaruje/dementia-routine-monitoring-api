import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="EDRMS Dashboard", layout="wide")

st.title("Early Dementia Routine Monitoring System (EDRMS)")
st.sidebar.header("Navigation")

page = st.sidebar.radio("Go to", ["Patients Overview", "Alerts & Anomalies"])

if page == "Patients Overview":
    st.header("Patient List")
    try:
        response = requests.get(f"{API_URL}/patients/")
        if response.status_code == 200:
            patients = response.json()
            if patients:
                df = pd.DataFrame(patients)
                st.dataframe(df)
                
                st.subheader("Patient Activities")
                selected_patient = st.selectbox("Select Patient ID", [p["id"] for p in patients])
                
                if selected_patient:
                    act_resp = requests.get(f"{API_URL}/activities/patient/{selected_patient}")
                    if act_resp.status_code == 200:
                        activities = act_resp.json()
                        if activities:
                            act_df = pd.DataFrame(activities)
                            st.dataframe(act_df)
                        else:
                            st.info("No activities found for this patient.")
            else:
                st.info("No patients found.")
    except Exception as e:
        st.error(f"Error connecting to API: {e}")

elif page == "Alerts & Anomalies":
    st.header("Recent Alerts")
    try:
        response = requests.get(f"{API_URL}/alerts/")
        if response.status_code == 200:
            alerts = response.json()
            if alerts:
                for alert in alerts:
                    severity_color = "red" if alert["severity"] == "high" else ("orange" if alert["severity"] == "medium" else "blue")
                    st.markdown(f"**Patient ID {alert['patient_id']}** - <span style='color:{severity_color}'>{alert['severity'].upper()}</span>: {alert['message']} ({alert['timestamp']})", unsafe_allow_html=True)
            else:
                st.success("No alerts found.")
                
        st.subheader("Run ML Anomaly Detection")
        patient_id = st.number_input("Patient ID", min_value=1, step=1)
        if st.button("Run Detection"):
            with st.spinner("Running ML Detection..."):
                res = requests.post(f"{API_URL}/alerts/patient/{patient_id}/run-ml-detection")
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"{data['message']} Found {data['anomalies_found']} anomalies.")
                else:
                    st.error("Failed to run detection.")
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
