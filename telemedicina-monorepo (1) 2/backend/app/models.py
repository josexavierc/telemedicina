from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum, Float, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base
import enum

user_specialty = Table(
    "user_specialty", Base.metadata,
    Column("clinician_id", Integer, ForeignKey("clinicians.id")),
    Column("specialty_id", Integer, ForeignKey("specialties.id"))
)

class RoleEnum(str, enum.Enum):
    admin = "admin"
    clinician = "clinician"
    patient = "patient"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, default="")
    role = Column(Enum(RoleEnum), default=RoleEnum.patient)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="user", uselist=False)
    clinician = relationship("Clinician", back_populates="user", uselist=False)

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    phone = Column(String, default="")
    tz = Column(String, default="America/Guayaquil")
    user = relationship("User", back_populates="patient")

class Clinician(Base):
    __tablename__ = "clinicians"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    license_number = Column(String, default="")
    bio = Column(Text, default="")
    user = relationship("User", back_populates="clinician")
    specialties = relationship("Specialty", secondary=user_specialty, back_populates="clinicians")

class Specialty(Base):
    __tablename__ = "specialties"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, default="")
    clinicians = relationship("Clinician", secondary=user_specialty, back_populates="specialties")

class Clinic(Base):
    __tablename__ = "clinics"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, default="")

class AppointmentStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    canceled = "canceled"
    completed = "completed"
    no_show = "no_show"

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    clinician_id = Column(Integer, ForeignKey("clinicians.id"))
    scheduled_at = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=30)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.pending)
    notes = Column(Text, default="")
    room_id = Column(String, index=True)

class Availability(Base):
    __tablename__ = "availability"
    id = Column(Integer, primary_key=True)
    clinician_id = Column(Integer, ForeignKey("clinicians.id"))
    weekday = Column(Integer)  # 0-6
    start_hour = Column(Integer)  # 0-23
    end_hour = Column(Integer)    # 0-23

class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    pdf_path = Column(String)
    icd10_code = Column(String, default="")
    meds = Column(Text, default="")

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    owner_user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    path = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class PaymentProvider(str, enum.Enum):
    stripe = "stripe"
    mercadopago = "mercadopago"
    simulated = "simulated"

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    amount = Column(Float, default=0.0)
    currency = Column(String, default="usd")
    provider = Column(Enum(PaymentProvider), default=PaymentProvider.stripe)
    external_id = Column(String, default="")
    status = Column(String, default="created")
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String)
    path = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip = Column(String, default="")
    user_agent = Column(String, default="")
