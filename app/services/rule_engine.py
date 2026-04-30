from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app import models
from app.services.alert_service import create_alert

def process_activity_rules(activity: models.activity.Activity, db: Session):
    patient_id = activity.patient_id
    
    # Rule 1: Medication missed -> Immediate Alert
    if activity.activity_type == "medication" and activity.status == "missed":
        create_alert(
            db=db,
            patient_id=patient_id,
            alert_type="medication_missed",
            severity="high",
            message=f"Patient missed scheduled medication at {activity.timestamp}"
        )
        
    # Rule 2: Missed meal >= 2 times in 24h
    if activity.activity_type == "meal" and activity.status == "missed":
        # Check last 24 hours
        time_threshold = activity.timestamp - timedelta(hours=24)
        missed_meals_count = db.query(models.activity.Activity).filter(
            models.activity.Activity.patient_id == patient_id,
            models.activity.Activity.activity_type == "meal",
            models.activity.Activity.status == "missed",
            models.activity.Activity.timestamp >= time_threshold
        ).count()
        
        if missed_meals_count >= 2:
            create_alert(
                db=db,
                patient_id=patient_id,
                alert_type="repeated_missed_meals",
                severity="medium",
                message=f"Patient missed {missed_meals_count} meals in the last 24 hours."
            )
            
    # Rule 3: Sleep deviation
    if activity.activity_type == "sleep" and activity.status == "delayed":
        create_alert(
            db=db,
            patient_id=patient_id,
            alert_type="sleep_delayed",
            severity="low",
            message=f"Patient sleep schedule was delayed at {activity.timestamp}"
        )
