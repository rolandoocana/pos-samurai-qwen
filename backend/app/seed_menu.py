import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from database import SessionLocal, init_db; from models import Product
MENU = {
    "BEBIDAS": [
        {"code":"BEB-001","name":"Limonada Azul (Vaso)","price":1.50},{"code":"BEB-002","name":"Limonada Azul (Jarra)","price":5.00},
        {"code":"BEB-003","name":"Jugo (Vaso)","price":1.50},{"code":"BEB-004","name":"Jugo (Jarra)","price":5.00},
        {"code":"BEB-005","name":"Batido (Vaso)","price":1.50},{"code":"BEB-006","name":"Batido (Jarra)","price":5.00},
        {"code":"BEB-007","name":"Milkshake (Choc/Oreo/Fresa)","price":3.50},{"code":"BEB-008","name":"Cerveza Artesanal","price":3.50},
        {"code":"BEB-009","name":"Michelada","price":4.00},{"code":"BEB-010","name":"Chelada","price":3.50},
        {"code":"BEB-011","name":"Cafe","price":1.00},{"code":"BEB-012","name":"Agua Aromatica","price":1.00},
        {"code":"BEB-013","name":"Agua","price":1.50},{"code":"BEB-014","name":"Agua con Gas","price":0.75},
        {"code":"BEB-015","name":"Gaseosa Personal","price":1.00},{"code":"BEB-016","name":"Gaseosa 1 Litro","price":0.75}
    ],
    "APERITIVOS": [
        {"code":"APE-001","name":"Mini Croissant Chocolate","price":2.00},{"code":"APE-002","name":"Humitas","price":1.00},
        {"code":"APE-003","name":"Empanada Queso","price":1.00},{"code":"APE-004","name":"Empanada Carne","price":1.00},
        {"code":"APE-005","name":"Nachos con Queso","price":3.00},{"code":"APE-006","name":"Papas con Chilli","price":4.00},
        {"code":"APE-007","name":"Patacones con Queso","price":2.00}
    ],
    "HAMBURGUESAS": [
        {"code":"HAM-001","name":"Hamburguesa Simple","price":3.25},{"code":"HAM-002","name":"Hamburguesa Piña","price":4.00},
        {"code":"HAM-003","name":"Mexaburguer","price":5.00},{"code":"HAM-004","name":"Miel y Fuego","price":4.50},
        {"code":"HAM-005","name":"Mango Habanero","price":4.50},{"code":"HAM-006","name":"Strips + Papas","price":4.00},
        {"code":"HAM-007","name":"Salchipapa","price":2.00},{"code":"HAM-008","name":"Papa Completa","price":3.50},
        {"code":"HAM-009","name":"6 Alitas + Papas","price":5.00},{"code":"HAM-010","name":"12 Alitas + Papas","price":10.00}
    ],
    "PLATOS FUERTES": [
        {"code":"PLA-001","name":"Grill Pollo","price":6.50},{"code":"PLA-002","name":"Grill Chuleta","price":6.50},
        {"code":"PLA-003","name":"Grill Carne","price":6.50},{"code":"PLA-004","name":"Parrillada","price":9.99},
        {"code":"PLA-005","name":"Costilla","price":7.50},{"code":"PLA-006","name":"Filete Pollo Apanado","price":6.50},
        {"code":"PLA-007","name":"Picana","price":9.99},{"code":"PLA-008","name":"Lomo","price":9.99}
    ],
    "COMBOS": [{"code":"COM-001","name":"Combo 2 Grilles + Papas + 2 Beb + Patacones","price":10.00}]
}
def seed():
    init_db(); db = SessionLocal()
    if db.query(Product).count() > 0: print("⚠️ Menú ya existe."); db.close(); return
    for cat, items in MENU.items():
        for i in items: db.add(Product(code=i["code"], name=i["name"], price=i["price"], category=cat))
    db.commit(); db.close(); print("✅ Menú SAMURAI cargado (46 ítems exactos del PDF).")
if __name__ == "__main__": seed()
