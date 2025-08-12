# Telemedicina — Monorepo (FastAPI + Next.js)

Plataforma de telemedicina con catálogo de especialidades, agenda médica, teleconsulta (WebRTC), recetas PDF, pagos (Stripe sandbox), roles (admin/médico/paciente), reportes y notificaciones. Incluye Docker, CI básico y blueprints para Render.

## Estructura
```
/backend       # FastAPI, SQLAlchemy, JWT, WebSockets (señalización WebRTC), Stripe, ReportLab
/frontend      # Next.js + React + TypeScript + Tailwind + React Query
/infra         # docker-compose, render.yaml, GitHub Actions (build/test), seed y .env
/docs          # Guías de despliegue y configuración
```

## Inicio rápido (local con Docker)
1) **Requisitos**: Docker Desktop y Git.
2) **Instalar y sembrar datos**:
```bash
chmod +x install.sh
./install.sh
```
3) **Abrir**:
- Frontend: http://localhost:3000
- Backend:  http://localhost:8000/docs

**Credenciales demo** (se crean con el seed):
- Admin:    jcobo@fidelity-ec.com / Admin123!
- Médico:   medico@demo.local / Medico123!
- Paciente: paciente@demo.local / Paciente123!

## Despliegue en Render (gratuito)
Sigue `/docs/DEPLOY_RENDER.md`. Usa `infra/render.yaml` (Blueprint). Render crea:
- Postgres (Free)
- Redis (Free)
- Backend (Web service Docker)
- Frontend (Web service Node)
Configura las variables de entorno solicitadas (Stripe test key, SendGrid/Twilio sandbox).

## Pagos (Stripe - modo test)
- Usa claves de prueba que empiezan con `sk_test_...`. No se realizan cargos reales.
- Cambiar a producción: ver `/docs/CONFIG_PAGOS.md`.

## Seguridad
- HTTPS lo entrega Render automáticamente en el dominio gratuito.
- JWT con expiración configurable, CORS restrictivo, auditoría de accesos.


**Calendario:** endpoint `/calendar/links/{appointment_id}` devuelve enlaces a Google, Outlook y un ICS embebido.
