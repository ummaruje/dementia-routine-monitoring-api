from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import database, models, schemas
# We'll import rule engine later

router = APIRouter(prefix="/activities", tags=["Activities"])

@router.post("/", response_model=schemas.activity.ActivityResponse)
def log_activity(activity: schemas.activity.ActivityCreate, db: Session = Depends(database.get_db)):
    # Verify patient exists
    patient = db.query(models.patient.Patient).filter(models.patient.Patient.id == activity.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db_activity = models.activity.Activity(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    # Trigger rule engine check
    from app.services.rule_engine import process_activity_rules
    process_activity_rules(db_activity, db)

    return db_activity

@router.get("/patient/{patient_id}", response_model=List[schemas.activity.ActivityResponse])
def get_patient_activities(patient_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    activities = db.query(models.activity.Activity).filter(models.activity.Activity.patient_id == patient_id).order_by(models.activity.Activity.timestamp.desc()).offset(skip).limit(limit).all()
    return activities
