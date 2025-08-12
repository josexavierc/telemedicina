from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .db import get_db
from .schemas import Token, UserCreate, UserOut
from . import models
from .auth import get_password_hash, create_access_token, verify_password, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db), current: models.User | None = Depends(lambda: None)):
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email ya existe")
    user = models.User(email=payload.email, full_name=payload.full_name or "", hashed_password=get_password_hash(payload.password), role=payload.role)
    db.add(user); db.commit(); db.refresh(user)
    if payload.role == models.RoleEnum.patient:
        db.add(models.Patient(user_id=user.id)); db.commit()
    elif payload.role == models.RoleEnum.clinician:
        db.add(models.Clinician(user_id=user.id)); db.commit()
    return user

@router.post("/token", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return {"access_token": token}
