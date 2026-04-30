from pydantic import BaseModel
from datetime import datetime

class ActivityBase(BaseModel):
    patient_id: int
    activity_type: str
    timestamp: datetime
    status: str

class ActivityCreate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: int

    class Config:
        from_attributes = True
