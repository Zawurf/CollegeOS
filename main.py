from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from engines.collegeos_runner import run_college_os
from models import context
from datetime import datetime
from database.database import (
    get_subject_id,
    add_daily_logs,
    is_already_logged
)
from config import COLLEGEOS_TOKEN

app = FastAPI(title="College OS")

class LocationInput(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)


class AttendanceResponse(BaseModel):
    subject: str
    response: str
    hours: int = 1
    start_time: str
    end_time: str

@app.post("/location")
def run_system(location: LocationInput):
    print("Received location:", location.lat, location.lon)

    context = run_college_os(
        latitude=location.lat,
        longitude=location.lon,
    )

    return {
        "current_class": context.current_class,
        "attendance": context.attendance,
        "location": context.location,
        "confidence": context.confidence,
        "notifications": context.notifications
    }

@app.post("/attendance-response")
def attendance_response(
    data: AttendanceResponse,
    x_collegeos_token: str = Header(None)
):
    if x_collegeos_token != COLLEGEOS_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if data.response.upper() == "YES":
        sub_id = get_subject_id(data.subject)

        if sub_id is None:
            return {
                "status": "error",
                "message": f"Subject not found: {data.subject}"
            }

        today = datetime.now().strftime("%Y-%m-%d")

        if is_already_logged(
                sub_id,
                today,
                data.start_time,
                data.end_time
        ):
            return {
                "status": "already_logged",
                "message": f"Attendance already logged for {data.subject}"
            }

        add_daily_logs(
            sub_id,
            today,
            "present",
            data.hours,
            data.start_time,
            data.end_time
        )

        return {
            "status": "success",
            "message": f"Attendance marked: {data.subject}"
        }

    
    elif data.response.upper() == 'NO':
        return{
            "status": "Success",
            "message": f"Attendance not marked: {data.subject}",
        }

    return{
        "status" : "error",
        "message" : "Invalid response. Use YES or NO."
    }

#uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# cloudflared tunnel --url http://localhost:8000