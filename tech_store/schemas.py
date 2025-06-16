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

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str  # plain password here

class User(UserBase):
    id: int
    is_active: Optional[int]

    class Config:
        orm_mode = True

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
        orm_mode = True

class InvoiceBase(BaseModel):
    order_id: int

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int
    total_amount: float
    issued_at: datetime
    product_name: str
    product_price: float
    order_created_at: datetime

    class Config:
        orm_mode = True


class InvoiceResponse(BaseModel):
    id: int
    order_id: int
    total_amount: float
    issued_at: datetime
    product_name: str
    product_price: float
    order_created_at: datetime

    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

