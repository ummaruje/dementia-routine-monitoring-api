import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_edrms_alerts.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_medication_missed_alert():
    # Create patient
    res = client.post("/patients/", json={"name": "Alert Patient", "age": 75, "diagnosis_stage": "Mid"})
    patient_id = res.json()["id"]
    
    # Log missed medication
    res = client.post("/activities/", json={
        "patient_id": patient_id, 
        "activity_type": "medication", 
        "timestamp": datetime.utcnow().isoformat(), 
        "status": "missed"
    })
    assert res.status_code == 200
    
    # Check if alert was generated
    alerts_res = client.get(f"/alerts/patient/{patient_id}")
    assert alerts_res.status_code == 200
    alerts = alerts_res.json()
    assert len(alerts) > 0
    assert alerts[0]["alert_type"] == "medication_missed"
    assert alerts[0]["severity"] == "high"
