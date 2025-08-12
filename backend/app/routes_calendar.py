from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from urllib.parse import urlencode, quote
from .db import get_db
from . import models
from .auth import get_current_user

router = APIRouter(prefix="/calendar", tags=["calendar"])

def _format_dt(dt: datetime) -> str:
    # Google requires UTC-like 'YYYYMMDDTHHMMSSZ'; assume naive dt is UTC for demo
    return dt.strftime('%Y%m%dT%H%M%SZ')

@router.get("/links/{appointment_id}")
def calendar_links(appointment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    a = db.query(models.Appointment).get(appointment_id)
    if not a: raise HTTPException(404, "Cita no encontrada")
    start = a.scheduled_at
    end = a.scheduled_at + timedelta(minutes=a.duration_minutes or 30)
    title = "Teleconsulta médica"
    details = f"Teleconsulta. Sala: {a.room_id}"
    location = "Online"

    # Google Calendar
    g_params = {
        "action": "TEMPLATE",
        "text": title,
        "details": details,
        "location": location,
        "dates": f"{_format_dt(start)}/{_format_dt(end)}"
    }
    google = "https://www.google.com/calendar/render?" + urlencode(g_params)

    # Outlook Web (Office/Microsoft 365)
    o_params = {
        "path": "/calendar/action/compose",
        "rru": "addevent",
        "subject": title,
        "body": details,
        "startdt": start.isoformat(),
        "enddt": end.isoformat(),
        "location": location
    }
    outlook = "https://outlook.office.com/calendar/0/deeplink/compose?" + urlencode(o_params)

    # ICS content
    ics = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Telemed//ES
BEGIN:VEVENT
UID:telemed-{a.id}
DTSTAMP:{_format_dt(datetime.utcnow())}
DTSTART:{_format_dt(start)}
DTEND:{_format_dt(end)}
SUMMARY:{title}
DESCRIPTION:{details}
LOCATION:{location}
END:VEVENT
END:VCALENDAR
"""
    return {"google": google, "outlook": outlook, "ics": ics}
