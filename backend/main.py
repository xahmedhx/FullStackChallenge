from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from database import engine, get_db, Base
from models import SensorReading
from schemas import SensorReadingCreate, SensorReadingResponse

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
def create_reading(reading: SensorReadingCreate, db: Session = Depends(get_db)):
    # Create new reading
    db_reading = SensorReading(**reading.dict())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    
    # Check if critical
    is_critical = False
    if reading.sensor_type == "Thermal" and reading.value > 75:
        is_critical = True
    elif reading.sensor_type == "Vibration" and reading.value > 5.0:
        is_critical = True
    
    # Create response
    response = SensorReadingResponse(
        id=db_reading.id,
        sensor_type=db_reading.sensor_type,
        value=db_reading.value,
        location=db_reading.location,
        timestamp=db_reading.timestamp,
        is_critical=is_critical
    )
    
    return response

@app.get("/readings", response_model=List[SensorReadingResponse])
def get_readings(db: Session = Depends(get_db)):
    readings = db.query(SensorReading).order_by(SensorReading.timestamp.desc()).limit(20).all()
    
    # Add is_critical flag
    response = []
    for r in readings:
        is_critical = False
        if r.sensor_type == "Thermal" and r.value > 75:
            is_critical = True
        elif r.sensor_type == "Vibration" and r.value > 5.0:
            is_critical = True
            
        response.append(SensorReadingResponse(
            id=r.id,
            sensor_type=r.sensor_type,
            value=r.value,
            location=r.location,
            timestamp=r.timestamp,
            is_critical=is_critical
        ))
    
    return response

@app.get("/")
def root():
    return {"message": "MEP Infrastructure Hub API"}