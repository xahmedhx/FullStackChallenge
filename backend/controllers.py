from sqlalchemy.orm import Session
from models import SensorReading
from schemas import SensorReadingCreate, SensorReadingResponse
from typing import List

def create_reading(reading: SensorReadingCreate, db: Session):
    # Save to DB
    db_reading = SensorReading(**reading.dict())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    
    # Check critical
    is_critical = False
    if reading.sensor_type == "Thermal" and reading.value > 75:
        is_critical = True
    elif reading.sensor_type == "Vibration" and reading.value > 5.0:
        is_critical = True
    
    return SensorReadingResponse(
        id=db_reading.id,
        sensor_type=db_reading.sensor_type,
        value=db_reading.value,
        location=db_reading.location,
        timestamp=db_reading.timestamp,
        is_critical=is_critical
    )

def get_readings(db: Session):
    readings = db.query(SensorReading).order_by(
        SensorReading.timestamp.desc()
    ).limit(20).all()
    
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