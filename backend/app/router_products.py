from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import models, ws_manager, database
from typing import Dict
router = APIRouter(prefix="/api", tags=["products"])
@router.get("/products")
async def get_products(db: Session = Depends(database.get_db)): return db.query(models.Product).filter(models.Product.available == True).all()
@router.post("/products/bulk-prices")
async def bulk(prices: Dict[str, float], db: Session = Depends(database.get_db)):
    for pid, price in prices.items(): db.query(models.Product).filter(models.Product.id == pid).update({models.Product.price: price})
    db.commit()
    await ws_manager.broadcast(["kitchen", "cashier", "waiter"], {"type": "price_refresh"})
    return {"updated": len(prices)}
