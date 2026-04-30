import requests
import time
from datetime import datetime, timedelta
import random

BASE_URL = "http://127.0.0.1:8000"

def simulate_data():
    print("Simulating Patient Data...")
    
    # 1. Register User
    try:
        requests.post(f"{BASE_URL}/auth/register", json={
            "email": "doctor@example.com",
            "password": "password123",
            "role": "admin"
        })
    except:
        pass # Might already exist

    # 2. Create Patient
    patient_res = requests.post(f"{BASE_URL}/patients/", json={
        "name": "John Doe",
        "age": 78,
        "diagnosis_stage": "Early"
    })
    
    if patient_res.status_code != 200:
        print("Failed to create patient.")
        return
        
    patient_id = patient_res.json()["id"]
    print(f"Created Patient ID: {patient_id}")
    
    # 3. Log normal baseline (3 days)
    now = datetime.utcnow()
    for day in range(3):
        date = now - timedelta(days=3-day)
        
        # Meal
        requests.post(f"{BASE_URL}/activities/", json={
            "patient_id": patient_id,
            "activity_type": "meal",
            "timestamp": (date.replace(hour=8)).isoformat(),
            "status": "completed"
        })
        
        # Medication
        requests.post(f"{BASE_URL}/activities/", json={
            "patient_id": patient_id,
            "activity_type": "medication",
            "timestamp": (date.replace(hour=9)).isoformat(),
            "status": "completed"
        })
        
    # 4. Log anomalies (Today)
    print("Logging anomalous behavior...")
    
    # Missed medication
    requests.post(f"{BASE_URL}/activities/", json={
        "patient_id": patient_id,
        "activity_type": "medication",
        "timestamp": now.replace(hour=9).isoformat(),
        "status": "missed"
    })
    
    # Missed meals
    requests.post(f"{BASE_URL}/activities/", json={
        "patient_id": patient_id,
        "activity_type": "meal",
        "timestamp": now.replace(hour=8).isoformat(),
        "status": "missed"
    })
    
    requests.post(f"{BASE_URL}/activities/", json={
        "patient_id": patient_id,
        "activity_type": "meal",
        "timestamp": now.replace(hour=13).isoformat(),
        "status": "missed"
    })
    
    print("Simulation complete. Check alerts endpoints.")

if __name__ == "__main__":
    simulate_data()
