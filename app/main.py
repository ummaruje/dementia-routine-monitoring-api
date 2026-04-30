from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import app.models  # Register models

from app.api import auth, patients, activities, alerts

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Early Dementia Routine Monitoring System (EDRMS)",
    description="API for tracking patient activities, modeling behaviour, and generating alerts.",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(activities.router)
app.include_router(alerts.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to EDRMS API"}
