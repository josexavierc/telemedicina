from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .db import get_db
from .schemas import SpecialtyBase, SpecialtyOut
from . import models
from .auth import get_current_user

router = APIRouter(prefix="/specialties", tags=["specialties"])

@router.get("/", response_model=List[SpecialtyOut])
def list_specialties(q: str | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(models.Specialty)
    if q:
        query = query.filter(models.Specialty.name.ilike(f"%{q}%"))
    return query.order_by(models.Specialty.name.asc()).all()

@router.post("/", response_model=SpecialtyOut)
def create_specialty(payload: SpecialtyBase, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Solo admin")
    spec = models.Specialty(name=payload.name, description=payload.description or "")
    db.add(spec); db.commit(); db.refresh(spec)
    return spec

@router.put("/{spec_id}", response_model=SpecialtyOut)
def update_specialty(spec_id: int, payload: SpecialtyBase, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Solo admin")
    spec = db.query(models.Specialty).get(spec_id)
    if not spec: raise HTTPException(status_code=404, detail="No existe")
    spec.name = payload.name; spec.description = payload.description or ""
    db.commit(); db.refresh(spec); return spec

@router.delete("/{spec_id}")
def delete_specialty(spec_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Solo admin")
    spec = db.query(models.Specialty).get(spec_id)
    if not spec: raise HTTPException(status_code=404, detail="No existe")
    db.delete(spec); db.commit(); return {"ok": True}
