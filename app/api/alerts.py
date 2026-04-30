from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import database, models, schemas
from app.ml.anomaly_detector import ActivityAnomalyDetector

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/", response_model=List[schemas.alert.AlertResponse])
def get_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    alerts = db.query(models.alert.Alert).order_by(models.alert.Alert.timestamp.desc()).offset(skip).limit(limit).all()
    return alerts

@router.get("/patient/{patient_id}", response_model=List[schemas.alert.AlertResponse])
def get_patient_alerts(patient_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    alerts = db.query(models.alert.Alert).filter(models.alert.Alert.patient_id == patient_id).order_by(models.alert.Alert.timestamp.desc()).offset(skip).limit(limit).all()
    return alerts

@router.post("/patient/{patient_id}/run-ml-detection")
def run_ml_detection(patient_id: int, db: Session = Depends(database.get_db)):
    # Run the isolation forest to find anomalies
    detector = ActivityAnomalyDetector(db, patient_id)
    anomalies = detector.train_and_predict()
    
    return {"message": "ML detection complete", "anomalies_found": len(anomalies)}
