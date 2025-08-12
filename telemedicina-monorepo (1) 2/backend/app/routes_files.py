from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime
from .db import get_db
from .config import get_settings
from . import models
from .auth import get_current_user

router = APIRouter(prefix="/files", tags=["files"])
settings = get_settings()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    dest_dir = Path(settings.FILE_STORAGE_PATH) / "uploads"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{int(datetime.utcnow().timestamp())}_{file.filename}"
    with open(dest, "wb") as f:
        f.write(await file.read())
    doc = models.Document(owner_user_id=user.id, filename=file.filename, path=str(dest))
    db.add(doc); db.commit(); db.refresh(doc)
    return {"id": doc.id, "filename": doc.filename}
