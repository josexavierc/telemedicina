# Cambiar a tu dominio propio

En Render:
1. Abre el servicio `telemed-frontend`.
2. Ve a **Custom Domains** y añade tu dominio.
3. Configura los registros DNS (CNAME) que Render te indique.
4. Render emitirá TLS (Let's Encrypt) automáticamente.

Si el backend también requiere dominio propio, repite el proceso en `telemed-backend`.
