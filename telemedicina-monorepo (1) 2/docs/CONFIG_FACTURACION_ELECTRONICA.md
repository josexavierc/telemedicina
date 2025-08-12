# Facturación electrónica (opcional)

Este demo no incluye un PAC específico. Para Ecuador:
- Integra con un proveedor autorizado (ej. **Facturación Electrónica SRI** mediante un PAC).
- Crea un micro-servicio en backend que firme XML y envíe al SRI.
- Guarda PDF/ride en `/data` y asócialo a `Payment`.

Estructura recomendada:
- Tabla `invoices` con `claveAcceso`, `estadoSRI`, `pdf_path`.
- Endpoints `/invoices/emit` y `/invoices/status`.
