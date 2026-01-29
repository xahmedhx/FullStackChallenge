# Full Stack Sensor Monitoring Application

This project is a full-stack application consisting of a Flutter frontend (compatible with web and mobile) and a Python FastAPI backend. The application is designed to display and record sensor data, demonstrating a complete end-to-end vertical slice of a modern application.

## Tech Stack

- **Frontend:** Flutter, Dart
- **Backend:** Python, FastAPI, SQLAlchemy, SQLite, Pydantic (for data validation)

## Features

- View a list of the latest 20 sensor readings.
- Readings are updated in real-time (with a manual refresh).
- Critical readings (e.g., high temperature or vibration) are highlighted.
- A functional backend provides data via a REST API.
- Cross-platform frontend works on Android, iOS, and Web.

## Folder Structure

The project is organized into two main parts:

- `/frontend`: Contains the complete Flutter application for the user interface.
- `/backend`: Contains the FastAPI application, which provides the API and handles the database.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Flutter SDK:** [Installation Guide](https://flutter.dev/docs/get-started/install)
- **Python 3.8+** and `pip`: [Installation Guide](https://www.python.org/downloads/)
- **An IDE** like VS Code or Android Studio is recommended.

---

## Setup and Installation

Follow these steps to get the application running locally. You will need two separate terminal windows for the backend and frontend.

### 1. Backend Setup

First, let's get the Python server running.

```bash
# Navigate to the backend directory
cd backend

# Create and activate a Python virtual environment
# On macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate

# On Windows:
python -m venv .venv
.venv\Scripts\activate

# Install the required dependencies
pip install -r requirements.txt

# Seed the database with initial sample data
# This will create a `sensor_readings.db` file
python seed.py

# Start the FastAPI server
uvicorn main:app --reload
```

The backend server will now be running at `http://127.0.0.1:8000`. You can view the auto-generated API documentation by visiting `http://127.0.0.1:8000/docs` in your browser.

### 2. Frontend Setup

Now, let's run the Flutter application.

```bash
# In a new terminal, navigate to the frontend directory
cd frontend

# Install the Flutter dependencies
flutter pub get

# Run the application on your desired device
# (Chrome, Android Emulator, iOS Simulator, etc.)
flutter run
```

The Flutter application will start, connect to the backend, and display the sensor readings.

## API Endpoints

The backend exposes the following REST API endpoints:

- `GET /readings`: Retrieves the last 20 sensor readings from the database.
- `POST /readings`: Creates a new sensor reading.

**Example `POST` body:**
```json
{
  "sensor_type": "Thermal",
  "value": 65.5,
  "location": "hvac_1"
}
```

## Technical Challenges

The biggest technical challenges encountered were two-fold. Firstly, connecting the Flutter frontend running on an Android emulator to the local Python backend proved tricky, as `localhost` behaves differently on emulators. This required implementing platform-specific URL handling (`10.0.2.2` for Android emulators). Secondly, integrating and ensuring seamless communication between the FastAPI backend and the SQLite database using SQLAlchemy also presented a learning curve, particularly in managing sessions and data models effectively.