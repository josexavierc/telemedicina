from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import get_db
from .schemas import PaymentCreate
from . import models
from .auth import get_current_user
from .config import get_settings

import stripe
settings = get_settings()
if settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/create")
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    pay = models.Payment(amount=payload.amount, currency=payload.currency, appointment_id=payload.appointment_id)
    provider = payload.provider
    if provider == "stripe" and settings.STRIPE_SECRET_KEY and settings.STRIPE_SECRET_KEY.startswith("sk_"):
        # Create a PaymentIntent in test mode
        intent = stripe.PaymentIntent.create(amount=int(payload.amount*100), currency=payload.currency, payment_method_types=["card"])
        pay.provider = models.PaymentProvider.stripe; pay.external_id = intent.id; pay.status = intent.status
    else:
        pay.provider = models.PaymentProvider.simulated; pay.external_id = "sim-"+str(pay.amount); pay.status = "requires_payment_method"
    db.add(pay); db.commit(); db.refresh(pay)
    return {"id": pay.id, "provider": pay.provider.value, "status": pay.status, "external_id": pay.external_id}
