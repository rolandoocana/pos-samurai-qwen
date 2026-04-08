from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database
router = APIRouter(prefix="/api", tags=["clients"])
@router.get("/clients/search/{doc}")
async def search(doc: str, db: Session = Depends(database.get_db)):
    c = db.query(models.Client).filter(models.Client.document_id == doc).first()
    return {"found": bool(c), "name": c.name if c else "", "source": c.source if c else "LOCAL"}
@router.post("/clients")
async def save(c: schemas.ClientCreate, db: Session = Depends(database.get_db)):
    db.add(models.Client(**c.model_dump())); db.commit()
    return {"status": "saved"}
