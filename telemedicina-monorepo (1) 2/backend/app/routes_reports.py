from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from .db import get_db
from . import models

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/appointments_by_specialty")
def appointments_by_specialty(db: Session = Depends(get_db)):
    # Simplified: counts by clinician's first specialty
    q = db.query(models.Specialty.name, func.count(models.Appointment.id)).        join(models.user_specialty, models.Specialty.id == models.user_specialty.c.specialty_id).        join(models.Clinician, models.Clinician.id == models.user_specialty.c.clinician_id).        join(models.Appointment, models.Appointment.clinician_id == models.Clinician.id).        group_by(models.Specialty.name).all()
    return [{"specialty": n, "count": c} for n, c in q]

@router.get("/no_show_rate")
def no_show_rate(db: Session = Depends(get_db)):
    total = db.query(func.count(models.Appointment.id)).scalar() or 1
    no_show = db.query(func.count(models.Appointment.id)).filter(models.Appointment.status == models.AppointmentStatus.no_show).scalar() or 0
    return {"no_show_rate": no_show/total}
