from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .db import get_db
from .schemas import PrescriptionCreate
from . import models
from .auth import get_current_user
from .config import get_settings

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])
settings = get_settings()

@router.post("/generate")
def generate_pdf(payload: PrescriptionCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    app = db.query(models.Appointment).get(payload.appointment_id)
    if not app: raise HTTPException(status_code=404, detail="Cita no encontrada")
    out_dir = Path(settings.FILE_STORAGE_PATH) / "prescriptions"
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / f"rx_{app.id}.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    c.setTitle("Receta Electrónica")
    c.drawString(50, 800, "Receta Electrónica")
    c.drawString(50, 780, f"Cita: {app.id} — Paciente #{app.patient_id} — Médico #{app.clinician_id}")
    c.drawString(50, 760, f"ICD-10: {payload.icd10_code}")
    textobject = c.beginText(50, 740)
    for line in payload.meds.split("\n"):
        textobject.textLine(line)
    c.drawText(textobject)
    c.drawString(50, 100, "Firma Digital: (placeholder)")
    c.showPage(); c.save()

    rx = models.Prescription(appointment_id=app.id, pdf_path=str(pdf_path), icd10_code=payload.icd10_code, meds=payload.meds)
    db.add(rx); db.commit(); db.refresh(rx)
    return {"id": rx.id, "pdf_path": rx.pdf_path}
