from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
import datetime

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    diagnosis_stage = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
