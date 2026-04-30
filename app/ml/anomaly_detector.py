import pandas as pd
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session
from app import models

class ActivityAnomalyDetector:
    def __init__(self, db: Session, patient_id: int):
        self.db = db
        self.patient_id = patient_id
        self.model = IsolationForest(contamination=0.1, random_state=42)
        
    def _fetch_data(self):
        activities = self.db.query(models.activity.Activity).filter(
            models.activity.Activity.patient_id == self.patient_id
        ).all()
        
        if not activities:
            return pd.DataFrame()
            
        # Convert to DataFrame
        data = []
        for a in activities:
            data.append({
                "timestamp": a.timestamp,
                "hour_of_day": a.timestamp.hour,
                "activity_type": 0 if a.activity_type == "meal" else (1 if a.activity_type == "medication" else 2),
                "status": 0 if a.status == "completed" else (1 if a.status == "delayed" else 2)
            })
            
        return pd.DataFrame(data)

    def train_and_predict(self):
        df = self._fetch_data()
        if df.empty or len(df) < 10:
            return [] # Not enough data
            
        features = df[["hour_of_day", "activity_type", "status"]]
        self.model.fit(features)
        predictions = self.model.predict(features)
        
        anomalies = []
        for i, pred in enumerate(predictions):
            if pred == -1: # Anomaly detected
                anomalies.append(df.iloc[i].to_dict())
                
        return anomalies
