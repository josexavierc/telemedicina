from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .models import RoleEnum, AppointmentStatus

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = ""

class UserCreate(UserBase):
    password: str
    role: RoleEnum

class UserOut(UserBase):
    id: int
    role: RoleEnum
    class Config:
        from_attributes = True

class SpecialtyBase(BaseModel):
    name: str
    description: str = ""

class SpecialtyOut(SpecialtyBase):
    id: int
    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    patient_id: int
    clinician_id: int
    scheduled_at: datetime
    duration_minutes: int = 30

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    clinician_id: int
    scheduled_at: datetime
    duration_minutes: int
    status: AppointmentStatus
    room_id: str | None = None
    class Config:
        from_attributes = True

class PrescriptionCreate(BaseModel):
    appointment_id: int
    icd10_code: str = ""
    meds: str = ""

class PaymentCreate(BaseModel):
    amount: float
    currency: str = "usd"
    appointment_id: int | None = None
    provider: str = "stripe"
