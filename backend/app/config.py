import os
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "pos.db")
JWT_SECRET = os.getenv("JWT_SECRET", "samurai_pos_lan_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
SRI_ENV = os.getenv("SRI_ENV", "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl")
PRINTER_NAME = os.getenv("PRINTER_NAME", None)
