from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from . import models, schemas, ws_manager, database, printer_service, sri_engine
import json
router = APIRouter(prefix="/api", tags=["orders"])
@router.post("/orders", status_code=201)
async def create_order(order: schemas.OrderCreate, bg: BackgroundTasks, db: Session = Depends(database.get_db)):
    db_order = models.Order(table=order.table, takeout=order.takeout, subtotal=0, iva=0, total=0)
    db.add(db_order); db.commit(); db.refresh(db_order)
    total = 0
    for item in order.items:
        prod = db.query(models.Product).filter(models.Product.id == item.product_id, models.Product.available == True).first()
        if not prod: raise HTTPException(400, "Producto no disponible")
        db.add(models.OrderItem(order_id=db_order.id, product_id=prod.id, quantity=item.quantity, notes=json.dumps(item.notes), unit_price=prod.price))
        total += prod.price * item.quantity
    iva = round(total * 0.15, 2)
    db_order.subtotal = round(total, 2); db_order.iva = iva; db_order.total = round(total + iva, 2)
    db.commit()
    await ws_manager.broadcast(["kitchen"], {"type": "new_order", "order_id": db_order.id, "table": db_order.table, "takeout": db_order.takeout})
    return {"order_id": db_order.id}
@router.patch("/orders/{order_id}/items/{item_id}")
async def update_item(item_id: str, status: str, db: Session = Depends(database.get_db)):
    it = db.query(models.OrderItem).filter(models.OrderItem.id == item_id).first()
    if not it: raise HTTPException(404)
    it.status = status; db.commit()
    await ws_manager.broadcast(["kitchen", "cashier"], {"type": "item_status", "item_id": item_id, "status": status})
    return {"status": "ok"}
@router.post("/orders/{order_id}/pay")
async def pay_order(order_id: str, payment: schemas.PaymentCreate, bg: BackgroundTasks, db: Session = Depends(database.get_db)):
    o = db.query(models.Order).filter(models.Order.id == order_id, models.Order.status == "PENDING").first()
    if not o: raise HTTPException(400, "Pedido no válido")
    o.status = "PAID"
    db.add(models.Payment(order_id=o.id, method=payment.method, amount=payment.amount))
    db.commit()
    bg.add_task(printer_service.queue_print, order_id)
    if payment.client_doc: bg.add_task(sri_engine.generate, order_id, payment.client_doc)
    return {"status": "paid"}
