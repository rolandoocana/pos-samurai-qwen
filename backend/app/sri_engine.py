import os, uuid
from datetime import datetime
from . import database, models
def generate(order_id: str, client_doc: str):
    db = next(database.get_db())
    o = db.query(models.Order).filter(models.Order.id == order_id).first()
    c = db.query(models.Client).filter(models.Client.document_id == client_doc).first()
    db.close()
    clave = f"{datetime.now().strftime('%d%m%Y')}0117912345670011001001000000{uuid.uuid4().hex[:5]}"
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<factura xmlns="http://sri.gob.ec/comprobantes/v2.0.0" id="comprobante">
  <infoTributaria><ambiente>1</ambiente><tipoEmision>1</tipoEmision><razonSocial>SAMURAI</razonSocial><ruc>1791234567001</ruc><claveAcceso>{clave}</claveAcceso><codDoc>01</codDoc><estab>001</estab><ptoEmi>001</ptoEmi><secuencial>000000001</secuencial></infoTributaria>
  <infoFactura><fechaEmision>{datetime.now().strftime('%d/%m/%Y')}</fechaEmision><totalSinImpuestos>{o.subtotal}</totalSinImpuestos><importeTotal>{o.total}</importeTotal></infoFactura>
</factura>'''
    path = os.path.join("backend", "sri_xml", f"{order_id}.xml")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: f.write(xml)
    db = next(database.get_db())
    db.add(models.Invoice(order_id=order_id, client_doc=client_doc, clave_acceso=clave, xml_path=path, sri_status="AUTHORIZED"))
    db.commit(); db.close()
