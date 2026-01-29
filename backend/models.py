from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class SensorReading(Base):
    __tablename__ = "sensor_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    sensor_type = Column(String)
    value = Column(Float)
    location = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)