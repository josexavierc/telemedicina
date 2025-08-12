# Configurar Pagos

## Stripe (Test)
1. Crea cuenta en Stripe y activa modo test.
2. Copia tu `sk_test_...` a `STRIPE_SECRET_KEY` en el backend.
3. En frontend, no se requiere clave pública para el flujo básico de PaymentIntent (este demo crea el intent en backend).
4. Para producción, cambia a `sk_live_...` y configura webhooks si lo deseas.

## MercadoPago
Este es un placeholder en el demo. Se puede integrar creando un `Preference` desde backend y redirigiendo al checkout MP. 
