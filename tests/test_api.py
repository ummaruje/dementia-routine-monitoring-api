import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_edrms.db"

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

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to EDRMS API"}

def test_create_patient():
    response = client.post(
        "/patients/",
        json={"name": "Test Patient", "age": 80, "diagnosis_stage": "Early"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Patient"
    assert "id" in response.json()

def test_log_activity():
    response = client.post(
        "/activities/",
        json={"patient_id": 1, "activity_type": "meal", "timestamp": "2024-01-01T08:00:00", "status": "completed"}
    )
    assert response.status_code == 200
    assert response.json()["activity_type"] == "meal"
