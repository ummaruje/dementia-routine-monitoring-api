from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import database, models, schemas

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=schemas.patient.PatientResponse)
def create_patient(patient: schemas.patient.PatientCreate, db: Session = Depends(database.get_db)):
    db_patient = models.patient.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/", response_model=List[schemas.patient.PatientResponse])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    patients = db.query(models.patient.Patient).offset(skip).limit(limit).all()
    return patients

@router.get("/{patient_id}", response_model=schemas.patient.PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(database.get_db)):
    patient = db.query(models.patient.Patient).filter(models.patient.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
