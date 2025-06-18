from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from datetime import datetime, timezone
from typing import Optional, List

# знижка
def calculate_discount(product: models.Product):
    days_old = (datetime.now(timezone.utc) - product.created_at.replace(tzinfo=timezone.utc)).days
    discount_value = 0.2 if days_old > 30 else 0.0
    discounted_price = round(product.price * (1 - discount_value), 3)
    return discount_value, discounted_price

# хелпер для InvoiceDetailed

def build_invoice_detailed(invoice: models.Invoice, order: models.Order, product: models.Product) -> schemas.InvoiceDetailed:
    discount_value, discounted_price = calculate_discount(product)
    return schemas.InvoiceDetailed(
        id=invoice.id,
        order_id=invoice.order_id,
        total_amount=invoice.total_amount,
        issued_at=invoice.issued_at,
        discount=discount_value,
        discount_display=f"{discount_value*100:.0f}%",
        order_created_at=order.created_at,
        paid_at=order.paid_at,
        product_name=product.name,
        product_price=product.price
    )

# продукти
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict(), created_at=datetime.now(timezone.utc))
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.Product]:
    orm_products = db.query(models.Product).offset(skip).limit(limit).all()
    return [schemas.Product.from_orm(prod) for prod in orm_products]

def get_product(db: Session, product_id: int) -> models.Product:
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# користувачі
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        password=user.password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# замовлення
def create_order(db: Session, order: schemas.OrderCreate, cashier_id: int) -> schemas.Order:
    product = get_product(db, order.product_id)
    db_order = models.Order(
        product_id=product.id,
        quantity=1,
        status="created",
        created_at=datetime.now(timezone.utc),
        cashier_id=cashier_id,
        consultant_id=order.consultant_id
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return schemas.Order.from_orm(db_order)

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def process_order(db: Session, order_id: int, user_id: int):
    order = get_order(db, order_id)
    if order.status != "created":
        raise HTTPException(status_code=400, detail="Order already processed or paid")

    order.status = "processed"
    order.processed_by = user_id
    order.processed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(order)
    return order

def pay_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    if order.status != "processed":
        return None

    order.status = "paid"
    order.paid_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(order)
    return order

# рахунки
def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    order = get_order(db, invoice.order_id)
    if order.status != "processed":
        raise HTTPException(status_code=400, detail="Order must be processed before invoicing")

    existing_invoice = db.query(models.Invoice).filter(models.Invoice.order_id == invoice.order_id).first()
    if existing_invoice:
        raise HTTPException(status_code=400, detail="Invoice already exists")

    product = get_product(db, order.product_id)
    discount_value, discounted_price = calculate_discount(product)
    total_amount = discounted_price

    new_invoice = models.Invoice(
        order_id=order.id,
        total_amount=total_amount,
        issued_at=datetime.now(timezone.utc)
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    return build_invoice_detailed(new_invoice, order, product)

def get_invoices(db: Session, skip: int = 0, limit: int = 100, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    query = db.query(models.Invoice)
    if start_date:
        query = query.filter(models.Invoice.issued_at >= start_date)
    if end_date:
        query = query.filter(models.Invoice.issued_at <= end_date)
    invoices = query.offset(skip).limit(limit).all()

    result = []
    for inv in invoices:
        order = get_order(db, inv.order_id)
        product = get_product(db, order.product_id)
        result.append(build_invoice_detailed(inv, order, product))

    return result

def get_invoice(db: Session, invoice_id: int):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    order = get_order(db, invoice.order_id)
    product = get_product(db, order.product_id)

    return build_invoice_detailed(invoice, order, product)

def pay_invoice(db: Session, invoice_id: int):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    order = get_order(db, invoice.order_id)
    if order.paid_at:
        raise HTTPException(status_code=400, detail="Invoice already paid")

    order.status = "paid"
    order.paid_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(order)

    product = get_product(db, order.product_id)
    return build_invoice_detailed(invoice, order, product)
