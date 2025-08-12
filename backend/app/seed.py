from .db import Base, engine, SessionLocal
from . import models
from .auth import get_password_hash

SPECIALTIES = [
    "Medicina General","Medicina Interna","Pediatría","Ginecología","Otorrinolaringología","Oftalmología",
    "Dermatología","Cardiología","Neumología","Gastroenterología","Endocrinología","Nefrología","Neurología",
    "Psiquiatría","Psicología Clínica","Traumatología","Reumatología","Urología","Oncología","Hematología",
    "Alergología","Infectología","Geriatría","Nutrición","Medicina Física y Rehabilitación","Terapia de Lenguaje",
    "Terapia Ocupacional","Genética Médica","Medicina del Deporte","Medicina del Trabajo","Radiología","Odontología"
]

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Specialties
    for name in SPECIALTIES:
        if not db.query(models.Specialty).filter_by(name=name).first():
            db.add(models.Specialty(name=name, description=f"Especialidad: {name}"))
    db.commit()
    # Users
    def ensure_user(email, password, role):
        u = db.query(models.User).filter_by(email=email).first()
        if not u:
            u = models.User(email=email, full_name=email.split("@")[0], hashed_password=get_password_hash(password), role=role)
            db.add(u); db.commit(); db.refresh(u)
            if role == models.RoleEnum.patient:
                db.add(models.Patient(user_id=u.id))
            elif role == models.RoleEnum.clinician:
                c = models.Clinician(user_id=u.id)
                # Attach first specialty
                spec = db.query(models.Specialty).first()
                if spec: c.specialties.append(spec)
                db.add(c)
            db.commit()
        return u

    admin = ensure_user("jcobo@fidelity-ec.com", "Admin123!", models.RoleEnum.admin)
    med   = ensure_user("medico@demo.local", "Medico123!", models.RoleEnum.clinician)
    pac   = ensure_user("paciente@demo.local", "Paciente123!", models.RoleEnum.patient)
    db.close()
    print("Seed completado. Admin/Medico/Paciente creados.")

if __name__ == "__main__":
    run()
