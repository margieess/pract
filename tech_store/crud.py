from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas

# ==============================
# Products
# ==============================
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# ==============================
# Orders
# ==============================
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100, start_date: datetime = None, end_date: datetime = None):
    query = db.query(models.Order)
    if start_date and end_date:
        query = query.filter(
            (models.Order.created_at >= start_date) & 
            (models.Order.created_at <= end_date)
        )
    return query.offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate, cashier_id: int):
    db_order = models.Order(
        **order.dict(),
        status="created",
        cashier_id=cashier_id,
        created_at=datetime.utcnow()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def process_order(db: Session, order_id: int, consultant_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order and db_order.status == "created":
        db_order.status = "processed"
        db_order.processed_at = datetime.utcnow()
        db_order.consultant_id = consultant_id
        db.commit()
        db.refresh(db_order)
        return db_order
    return None

def pay_order(db: Session, order_id: int, cashier_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order or order.status != "processed":
        return None  # оплатити можна лише оброблене замовлення

    order.status = "paid"
    order.paid_at = datetime.utcnow()
    order.cashier_id = cashier_id
    db.commit()
    db.refresh(order)
    return order

# ==============================
# Invoices
# ==============================
def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    db_order = db.query(models.Order).filter(models.Order.id == invoice.order_id).first()
    if not db_order or db_order.status != "processed":
        return None

    product = db_order.product
    discount = 0.2 if (datetime.utcnow() - product.created_at).days > 30 else 0
    amount = product.price * (1 - discount)

    db_invoice = models.Invoice(
        order_id=invoice.order_id,
        total_amount=amount,
        issued_at=datetime.utcnow(),
        product_name=product.name,
        product_price=product.price,
        order_created_at=db_order.created_at
    )

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_invoice(db: Session, invoice_id: int):
    return db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    db_order = db.query(models.Order).filter(models.Order.id == invoice.order_id).first()
    if not db_order or db_order.status != "processed":
        return None

    product = db_order.product
    now = datetime.utcnow()
    days_since_creation = (now - product.created_at).days
    discount = 0.2 if days_since_creation > 30 else 0.0
    total_amount = product.price * (1 - discount)

    db_invoice = models.Invoice(
        order_id=invoice.order_id,
        total_amount=total_amount,
        issued_at=now,
        product_name=product.name,
        product_price=product.price,
        order_created_at=db_order.created_at
    )

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

# ==============================
# Users
# ==============================
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        hashed_password=user.password,  # ⚠️ пароль зберігається у відкритому вигляді (небезпечно!)
        role=user.role,
        is_active=1
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
