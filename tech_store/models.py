from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="product")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # "cashier", "consultant", "accountant"
    is_active = Column(Integer, default=1)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    status = Column(String, default="created")  # created, processed, paid
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    cashier_id = Column(Integer, ForeignKey("users.id"))
    consultant_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    product = relationship("Product", back_populates="orders")
    cashier = relationship("User", foreign_keys=[cashier_id])
    consultant = relationship("User", foreign_keys=[consultant_id])
    invoice = relationship("Invoice", uselist=False, back_populates="order")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    total_amount = Column(Float)
    issued_at = Column(DateTime, default=datetime.utcnow)  # ← обовʼязково default!

    order = relationship("Order", back_populates="invoice")


    # ➕ додано для відображення деталей товару в рахунку
    product_name = Column(String)
    product_price = Column(Float)
    order_created_at = Column(DateTime)

    order = relationship("Order", back_populates="invoice")

