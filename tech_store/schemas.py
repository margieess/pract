"""
Pydantic-схеми для API системи управління замовленнями
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    role: str
    password: str

class User(BaseModel):
    id: int
    username: str
    role: str
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True
        from_attributes = True


class OrderCreate(BaseModel):
    product_id: int
    consultant_id: Optional[int] = None

class Order(BaseModel):
    id: int
    product_id: int
    quantity: int
    status: str
    created_at: datetime
    processed_at: Optional[datetime]
    paid_at: Optional[datetime]
    cashier_id: Optional[int]
    consultant_id: Optional[int]

    class Config:
        orm_mode = True
        from_attributes = True


class InvoiceCreate(BaseModel):
    order_id: int

class Invoice(BaseModel):
    id: int
    order_id: int
    total_amount: float
    issued_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class InvoiceDetailed(BaseModel):
    id: int
    order_id: int
    total_amount: float
    issued_at: datetime
    discount: float
    discount_display: Optional[str] = None
    order_created_at: datetime
    paid_at: Optional[datetime]
    product_name: str
    product_price: float

    class Config:
        orm_mode = True
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

