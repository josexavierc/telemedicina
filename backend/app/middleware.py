from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .db import SessionLocal
from . import models

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        try:
            db = SessionLocal()
            user_id = None
            # Best-effort: parse user id from Authorization if present (not verifying here)
            auth = request.headers.get("authorization", "")
            if auth.startswith("Bearer "):
                # avoid heavy decode; keep null
                pass
            log = models.AuditLog(
                user_id=user_id,
                action=request.method,
                path=request.url.path,
                ip=request.client.host if request.client else "",
                user_agent=request.headers.get("user-agent", ""),
            )
            db.add(log); db.commit()
        except Exception:
            pass
        finally:
            try:
                db.close()
            except Exception:
                pass
        return response
