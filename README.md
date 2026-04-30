# Early Dementia Routine Monitoring System (EDRMS)

## 1. Problem Context
Early-stage dementia is often misunderstood as primarily a memory issue. In practice, the earliest and most impactful signs are disruptions to daily routines (meals, sleep, medication) and reduced consistency in behaviour patterns. In real care settings, these issues are not detected early enough and are heavily dependent on subjective caregiver observation.

**EDRMS** addresses this by providing a backend-driven system that logs patient daily activities, models routine behaviour patterns, detects deviations over time, and generates alerts for caregivers.

## 2. Architecture
```text
Client (Caregiver Dashboard - Streamlit)
        ↓
API Layer (FastAPI)
        ↓
Service Layer (Python/SQLAlchemy)
        ↓
Detection Engine (Rules Engine & Isolation Forest ML)
        ↓
Database (SQLite)
```

## 3. Setup Instructions

### Prerequisites
- Python 3.10+
- Virtual Environment

### Installation
1. Navigate to the project root.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Simulate realistic patient data (run in a separate terminal with environment activated):
   ```bash
   python data/simulate_patient_data.py
   ```
3. View the Streamlit Caregiver Dashboard:
   ```bash
   streamlit run app/dashboard.py
   ```
   
The interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.

## 4. Example API Usage

### Log a Patient Activity
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/activities/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "patient_id": 1,
  "activity_type": "medication",
  "timestamp": "2024-05-15T09:00:00Z",
  "status": "missed"
}'
```

## 5. Sample Outputs

**Alert Generation (JSON):**
```json
[
  {
    "patient_id": 1,
    "alert_type": "medication_missed",
    "severity": "high",
    "message": "Patient missed scheduled medication at 2024-05-15 09:00:00",
    "id": 1,
    "timestamp": "2024-05-15T09:00:02.123456"
  }
]
```

## 6. Limitations
- **Not Clinically Validated:** This system is a technical demonstration and has not been subjected to clinical trials.
- **No Real-time Device Integration:** Data is currently ingested via API; it does not connect directly to IoT sensors or wearables.
- **Simplified ML Models:** The anomaly detection uses a baseline Isolation Forest. Production systems would require more complex sequence modeling.
- **No Regulatory Compliance:** This software is not compliant with medical device standards (e.g., HIPAA, GDPR for health data, FDA regulations).
