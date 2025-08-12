from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
from datetime import datetime
from .db import get_db
from .schemas import AppointmentCreate, AppointmentOut
from . import models
from .auth import get_current_user

from .config import get_settings
import http.client, json as _json, base64

settings = get_settings()

def _send_email_sendgrid(to_email: str, subject: str, content: str):
    if not settings.SENDGRID_API_KEY or settings.SENDGRID_API_KEY.startswith('SG.change_me'):
        return
    conn = http.client.HTTPSConnection("api.sendgrid.com")
    payload = _json.dumps({
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": settings.EMAIL_FROM},
        "subject": subject,
        "content": [{"type": "text/plain", "value": content}]
    })
    headers = {
        'Authorization': f'Bearer {settings.SENDGRID_API_KEY}',
        'Content-Type': "application/json"
    }
    conn.request("POST", "/v3/mail/send", payload, headers)
    _ = conn.getresponse()
    conn.close()

def _send_whatsapp_twilio(to_phone: str, body: str):
    # requires sandbox opt-in and E.164 numbers
    if not settings.TWILIO_ACCOUNT_SID or settings.TWILIO_ACCOUNT_SID.startswith('AC_change_me'):
        return
    acct = settings.TWILIO_ACCOUNT_SID
    token = settings.TWILIO_AUTH_TOKEN
    from_ = settings.TWILIO_WHATSAPP_FROM
    auth = base64.b64encode(f"{acct}:{token}".encode()).decode()
    conn = http.client.HTTPSConnection("api.twilio.com")
    payload = f"From={from_}&To=whatsapp:%2B00000000000&Body={body}".encode()  # replace To in real usage
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': "application/x-www-form-urlencoded"
    }
    conn.request("POST", f"/2010-04-01/Accounts/{acct}/Messages.json", payload, headers)
    _ = conn.getresponse()
    conn.close()


router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.post("/", response_model=AppointmentOut)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Basic overlap check omitted for brevity
    app = models.Appointment(
        patient_id=payload.patient_id,
        clinician_id=payload.clinician_id,
        scheduled_at=payload.scheduled_at,
        duration_minutes=payload.duration_minutes,
        status=models.AppointmentStatus.confirmed,
        room_id=str(uuid4())[:8],
    )
    db.add(app); db.commit(); db.refresh(app)

    # Notificaciones (best-effort)
    try:
        # Email
        _send_email_sendgrid("admin@demo.local", "Nueva cita creada",
                             f"Cita #{app.id} programada {app.scheduled_at} sala {app.room_id}")
    except Exception:
        pass
    return app

@router.get("/", response_model=List[AppointmentOut])
def list_my_appointments(db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(models.Appointment)
    if user.role == models.RoleEnum.patient:
        q = q.filter(models.Appointment.patient_id == user.patient.id)
    elif user.role == models.RoleEnum.clinician:
        q = q.filter(models.Appointment.clinician_id == user.clinician.id)
    return q.order_by(models.Appointment.scheduled_at.desc()).all()
