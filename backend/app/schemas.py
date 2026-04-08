from pydantic import BaseModel
from typing import List, Optional
class OrderItemCreate(BaseModel): product_id: str; quantity: int; notes: List[str] = []
class OrderCreate(BaseModel): table: Optional[int] = None; takeout: bool = False; items: List[OrderItemCreate]
class PaymentCreate(BaseModel): method: str; amount: float; client_doc: Optional[str] = None
class ClientCreate(BaseModel): document_id: str; name: str; source: str = "MANUAL"
class CashOpen(BaseModel): initial_cash: float; opened_by: str
class CashClose(BaseModel): actual_cash: float; closed_by: str; notes: Optional[str] = None
