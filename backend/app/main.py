from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .middleware import AuditMiddleware
from . import routes_auth, routes_specialties, routes_appointments, routes_payments, routes_files, routes_prescriptions, routes_reports, routes_video, routes_calendar
from . import seed

app = FastAPI(title="Telemed Backend")

# DB init (for demo; in prod use migrations)
Base.metadata.create_all(bind=engine)
# Ejecuta seed idempotente en arranque (demo/Render)
try:
    seed.run()
except Exception:
    pass

origins = ["http://localhost:3000", "http://127.0.0.1:3000", "*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(AuditMiddleware)

app.include_router(routes_auth.router)
app.include_router(routes_specialties.router)
app.include_router(routes_appointments.router)
app.include_router(routes_payments.router)
app.include_router(routes_files.router)
app.include_router(routes_prescriptions.router)
app.include_router(routes_reports.router)
app.include_router(routes_video.router)
app.include_router(routes_calendar.router)

@app.get("/healthz")
def healthz():
    return {"ok": True}
