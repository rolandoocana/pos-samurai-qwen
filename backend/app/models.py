from sqlalchemy import Column, String, Float, Boolean, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
import datetime, uuid
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True)
    hashed_pw = Column(String)
    role = Column(String)
class Client(Base):
    __tablename__ = "clients"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, unique=True, index=True)
    name = Column(String)
    source = Column(String, default="MANUAL")
class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String, unique=True)
    name = Column(String)
    price = Column(Float)
    category = Column(String)
    available = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    updated_by = Column(String, nullable=True)
class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    table = Column(Integer, nullable=True)
    takeout = Column(Boolean, default=False)
    status = Column(String, default="PENDING")
    subtotal = Column(Float)
    iva = Column(Float)
    total = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, ForeignKey("orders.id"))
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Integer)
    notes = Column(String)
    status = Column(String, default="PENDING")
    unit_price = Column(Float, nullable=False)
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, ForeignKey("orders.id"))
    method = Column(String)
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, unique=True)
    client_doc = Column(String)
    clave_acceso = Column(String, unique=True)
    xml_path = Column(String)
    sri_status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
class CashClosure(Base):
    __tablename__ = "cash_closures"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    opened_by = Column(String)
    closed_by = Column(String, nullable=True)
    opened_at = Column(DateTime, default=datetime.datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    initial_cash = Column(Float, default=0)
    expected_cash = Column(Float, default=0)
    actual_cash = Column(Float, default=0)
    discrepancy = Column(Float, default=0)
    status = Column(String, default="OPEN")
