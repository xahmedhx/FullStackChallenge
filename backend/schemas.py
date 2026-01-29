from pydantic import BaseModel
from datetime import datetime

class SensorReadingCreate(BaseModel):
    sensor_type: str
    value: float
    location: str

class SensorReadingResponse(BaseModel):
    id: int
    sensor_type: str
    value: float
    location: str
    timestamp: datetime
    is_critical: bool = False
    
    class Config:
        from_attributes = True