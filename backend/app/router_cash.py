from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
import datetime
router = APIRouter(prefix="/api", tags=["cash"])
@router.post("/cash/open")
async def open_cash(c: schemas.CashOpen, db: Session = Depends(database.get_db)):
    db.add(models.CashClosure(opened_by=c.opened_by, initial_cash=c.initial_cash)); db.commit(); return {"status": "opened"}
@router.post("/cash/close")
async def close_cash(closure_id: str, c: schemas.CashClose, db: Session = Depends(database.get_db)):
    cl = db.query(models.CashClosure).filter(models.CashClosure.id == closure_id, models.CashClosure.status == "OPEN").first()
    if not cl: raise HTTPException(404, "Caja no encontrada o ya cerrada")
    cl.closed_by = c.closed_by; cl.actual_cash = c.actual_cash; cl.closed_at = datetime.datetime.utcnow(); cl.status = "CLOSED"; db.commit()
    return {"status": "closed", "discrepancy": cl.actual_cash - cl.expected_cash}
