"""
SQLAlchemy-моделі для системи управління замовленнями
"""


from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    orders = relationship("Order", back_populates="product")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    cashier_orders = relationship("Order", back_populates="cashier", foreign_keys="Order.cashier_id")
    consultant_orders = relationship("Order", back_populates="consultant", foreign_keys="Order.consultant_id")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    status = Column(String, default="created")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    processed_at = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    cashier_id = Column(Integer, ForeignKey("users.id"))
    consultant_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    product = relationship("Product", back_populates="orders")
    cashier = relationship("User", back_populates="cashier_orders", foreign_keys=[cashier_id])
    consultant = relationship("User", back_populates="consultant_orders", foreign_keys=[consultant_id])
    invoice = relationship("Invoice", uselist=False, back_populates="order")

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    total_amount = Column(Float)
    issued_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    order = relationship("Order", back_populates="invoice")
