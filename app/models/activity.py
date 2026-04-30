from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    activity_type = Column(String, index=True) # meal, medication, sleep
    timestamp = Column(DateTime, index=True)
    status = Column(String) # completed, missed, delayed
    
    patient = relationship("Patient")
