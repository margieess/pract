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
        orm_mode  = True


class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str
    full_name: Optional[str] = None
    email: Optional[str] = None

class User(UserBase):
    id: int
    is_active: Optional[bool]

    class Config:
        orm_mode  = True


class OrderBase(BaseModel):
    product_id: int

class OrderCreate(OrderBase):
    consultant_id: Optional[int] = None

class Order(OrderBase):
    id: int
    quantity: int
    status: str
    created_at: datetime
    processed_at: Optional[datetime]
    paid_at: Optional[datetime]
    cashier_id: Optional[int]
    consultant_id: Optional[int]

    class Config:
        orm_mode  = True


class InvoiceCreate(BaseModel):
    order_id: int

class Invoice(BaseModel):
    id: int
    order_id: int
    total_amount: float
    issued_at: datetime

    class Config:
        orm_mode  = True

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
        orm_mode  = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

    class Config:
        orm_mode  = True