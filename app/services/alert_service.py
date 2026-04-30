from sqlalchemy.orm import Session
from app import models, schemas

def create_alert(db: Session, patient_id: int, alert_type: str, severity: str, message: str):
    alert_data = schemas.alert.AlertCreate(
        patient_id=patient_id,
        alert_type=alert_type,
        severity=severity,
        message=message
    )
    db_alert = models.alert.Alert(**alert_data.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert
