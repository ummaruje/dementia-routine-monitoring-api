from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    alert_type = Column(String, index=True)
    severity = Column(String) # low, medium, high
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    patient = relationship("Patient")
