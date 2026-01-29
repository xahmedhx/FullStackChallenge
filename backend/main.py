from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from database import engine, get_db, Base
from schemas import SensorReadingCreate, SensorReadingResponse
import controllers

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/readings", response_model=SensorReadingResponse)
def create_reading_endpoint(reading: SensorReadingCreate, db: Session = Depends(get_db)):
    return controllers.create_reading(reading, db)

@app.get("/readings", response_model=List[SensorReadingResponse])
def get_readings_endpoint(db: Session = Depends(get_db)):
    return controllers.get_readings(db)

@app.get("/")
def root():
    return {"message": "MEP Infrastructure Hub API"}