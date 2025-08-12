# Despliegue GRATIS en Render

1. Crea una cuenta en https://render.com (plan Free).
2. Crea un nuevo **Blueprint** y apunta al repositorio (sube este ZIP a GitHub primero).
3. Render leerá `infra/render.yaml` y propondrá crear:
   - Postgres (free)
   - Redis (free)
   - Web Service `telemed-backend` (Docker)
   - Web Service `telemed-frontend` (Node)
4. En `telemed-backend`, completa variables:
   - `STRIPE_SECRET_KEY` (modo test, comienza con `sk_test_`)
   - `SENDGRID_API_KEY` (opcional, sandbox)
   - `EMAIL_FROM`
5. Despliega. Render te dará dos URLs gratuitas (frontend y backend con HTTPS).
6. Verifica `NEXT_PUBLIC_API_BASE` en el frontend apunta al URL del backend (Render lo configura automáticamente con `fromService`).

**Usuarios demo** se crean con el seed inicial en el primer arranque.

**Nota:** el backend ejecuta el *seed* automáticamente en el primer arranque en Render.
