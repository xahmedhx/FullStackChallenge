import random
from datetime import datetime
from database import SessionLocal, engine
from models import SensorReading, Base

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

sensor_types = ["Thermal", "Vibration"]
locations = ["hvac_1", "hvac_2", "lighting_control_1", "lighting_control_2", "security_camera_1"]

for i in range(20):
    reading = SensorReading(
        sensor_type=random.choice(sensor_types),
        value=random.uniform(0.0, 100.0),
        location=random.choice(locations),
        timestamp=datetime.utcnow()
    )
    db.add(reading)

db.commit()
db.close()

print("Database seeded with 20 sensor readings.")
