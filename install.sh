#!/usr/bin/env bash
set -euo pipefail

echo "==> Creando archivos .env por defecto..."

mkdir -p backend/.envs frontend/.envs infra/.envs

# Backend .env
cat > backend/.env <<'EOF'
APP_NAME=telemed
ENV=dev
SECRET_KEY=please_change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120

DB_HOST=postgres
DB_PORT=5432
DB_NAME=telemed
DB_USER=telemed
DB_PASSWORD=telemed

REDIS_URL=redis://redis:6379/0
STRIPE_SECRET_KEY=sk_test_change_me
STRIPE_WEBHOOK_SECRET=whsec_change_me

SENDGRID_API_KEY=SG.change_me
EMAIL_FROM=no-reply@demo.local

TWILIO_ACCOUNT_SID=AC_change_me
TWILIO_AUTH_TOKEN=change_me
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886 # sandbox

FILE_STORAGE_PATH=/data
BASE_URL=http://localhost:8000
EOF

# Frontend .env
cat > frontend/.env.local <<'EOF'
NEXT_PUBLIC_APP_NAME=Telemed
NEXT_PUBLIC_API_BASE=http://localhost:8000
NEXT_PUBLIC_VIDEO_TURN_URL=
NEXT_PUBLIC_ENABLE_TWILIO_FALLBACK=false
EOF

# Docker Compose env (optional)
cat > infra/.envs/common.env <<'EOF'
POSTGRES_PASSWORD=telemed
POSTGRES_USER=telemed
POSTGRES_DB=telemed
EOF

echo "==> Construyendo y levantando contenedores (puede tardar)..."
docker compose -f infra/docker-compose.yml up -d --build

echo "==> Esperando base de datos..."
sleep 8

echo "==> Ejecutando seed inicial..."
docker compose -f infra/docker-compose.yml exec -T backend sh -c "python -m app.seed"

echo "==> Listo. Frontend en http://localhost:3000 — Backend en http://localhost:8000/docs"
