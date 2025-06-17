from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ---------- PRODUCTS ----------
class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

# ---------- USERS ----------
class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str  # plain text password

class User(UserBase):
    id: int
    is_active: Optional[bool]

    class Config:
        from_attributes = True

# ---------- ORDERS ----------
class OrderBase(BaseModel):
    product_id: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    status: str
    created_at: datetime
    processed_at: Optional[datetime]
    paid_at: Optional[datetime]
    cashier_id: Optional[int]
    consultant_id: Optional[int]

    class Config:
        from_attributes = True

# ---------- INVOICES ----------
class InvoiceCreate(BaseModel):
    order_id: int
    # total_amount: Optional[float] = None  # Додайте, якщо потрібно передавати суму

class Invoice(BaseModel):
    id: int
    order_id: int
    total_amount: float  # Змінено з amount на total_amount

    class Config:
        from_attributes = True

class InvoiceDetailed(BaseModel):
    id: int
    order_id: int
    total_amount: float  # Змінено з amount на total_amount
    discount: float
    discount_display: Optional[str] = None
    order_created_at: datetime
    paid_at: Optional[datetime]
    product_name: str
    product_price: float

    class Config:
        from_attributes = True

# ---------- AUTH ----------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

    class Config:
        from_attributes = True