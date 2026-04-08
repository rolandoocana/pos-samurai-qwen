import threading, time, json, win32print
from .database import get_db
from . import models
queue = []; lock = threading.Lock()
def queue_print(order_id: str):
    with lock: queue.append(order_id)
    threading.Thread(target=_worker, daemon=True).start()
def _worker():
    while True:
        with lock:
            if not queue: break
            oid = queue.pop(0)
        try: _raw_print(oid)
        except Exception as e: print(f"[PRINTER] {e}")
        time.sleep(0.5)
def _raw_print(oid: str):
    db = next(get_db())
    o = db.query(models.Order).filter(models.Order.id == oid).first()
    items = db.query(models.OrderItem, models.Product).join(models.Product).filter(models.OrderItem.order_id == oid).all()
    db.close()
    data = b"\x1B\x40\x1B\x61\x01RESTAURANTE SAMURAI\r\nRUC: 1791234567001\r\n"
    data += f"MESA: {o.table or 'LLEVAR'}\r\n".encode()
    data += b"--------------------------------\r\n"
    for it, prod in items:
        data += f"{it.quantity}x {prod.name} ${it.quantity*it.unit_price:.2f}\r\n".encode()
        notes = json.loads(it.notes)
        if notes:
            data += b"\x1B\x45\x01"
            for n in notes: data += f"  ⚠️ {n.upper()}\r\n".encode()
            data += b"\x1B\x45\x00"
    data += f"--------------------------------\r\nSUB: ${o.subtotal:.2f}\r\nIVA 15%: ${o.iva:.2f}\r\nTOTAL: ${o.total:.2f}\r\n".encode()
    data += b"\x1D\x56\x01"
    printer = win32print.GetDefaultPrinter()
    h = win32print.OpenPrinter(printer)
    try:
        win32print.StartDocPrinter(h, 1, ("POS", None, "RAW"))
        win32print.StartPagePrinter(h); win32print.WritePrinter(h, data)
        win32print.EndPagePrinter(h); win32print.EndDocPrinter(h)
    finally: win32print.ClosePrinter(h)
