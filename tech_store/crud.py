from sqlalchemy.orm import Session
from datetime import datetime, timezone
from . import models, schemas

# ---------------- PRODUCTS ----------------
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

# ---------------- USERS ----------------
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        hashed_password=user.password,  # plain text (рекомендується змінити на bcrypt)
        role=user.role,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# ---------------- ORDERS ----------------
def create_order(db: Session, order: schemas.OrderCreate, cashier_id: int):
    db_order = models.Order(
        product_id=order.product_id,
        created_at=datetime.now(timezone.utc),
        status="created",
        cashier_id=cashier_id
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def process_order(db: Session, order_id: int, user_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order or order.status != "created":
        return None
    order.status = "processed"
    order.processed_at = datetime.now(timezone.utc)
    order.consultant_id = user_id
    db.commit()
    db.refresh(order)
    return order

def pay_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order or order.status != "processed":
        return None
    order.status = "paid"
    order.paid_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(order)
    return order

# ---------------- INVOICES ----------------
def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    db_order = db.query(models.Order).filter(models.Order.id == invoice.order_id).first()
    if not db_order or db_order.status != "processed":
        return None

    product = db_order.product
    days_old = (datetime.now(timezone.utc) - product.created_at.replace(tzinfo=timezone.utc)).days
    discount_value = 0.2 if days_old > 30 else 0.0
    total_amount = round(product.price * (1 - discount_value), 3)

    db_invoice = models.Invoice(
        order_id=invoice.order_id,
        total_amount=total_amount
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    return {
        "id": db_invoice.id,
        "order_id": db_order.id,
        "total_amount": total_amount,
        "discount": discount_value,  # Залишаємо як float (0.2 або 0.0)
        "discount_display": f"{int(discount_value * 100)}%" if discount_value > 0 else "0%",  # Нове поле для відображення
        "order_created_at": db_order.created_at,
        "paid_at": db_order.paid_at,
        "product_name": product.name,
        "product_price": product.price
    }

def get_invoices(db: Session, skip: int = 0, limit: int = 100, start_date=None, end_date=None):
    query = db.query(models.Invoice).join(models.Order).join(models.Product)

    if start_date and end_date:
        query = query.filter(
            models.Order.created_at >= start_date,
            models.Order.created_at <= end_date
        )

    results = query.offset(skip).limit(limit).all()

    detailed = []
    for inv in results:
        product = inv.order.product
        order = inv.order
        days_old = (datetime.now(timezone.utc) - product.created_at.replace(tzinfo=timezone.utc)).days
        discount_value = 0.2 if days_old > 30 else 0.0
        total_amount = round(product.price * (1 - discount_value), 3)

        detailed.append(schemas.InvoiceDetailed(
            id=inv.id,
            order_id=order.id,
            total_amount=total_amount,
            discount=discount_value,  # Залишаємо як float
            discount_display=f"{int(discount_value * 100)}%" if discount_value > 0 else "0%",  # Нове поле
            order_created_at=order.created_at,
            paid_at=order.paid_at,
            product_name=product.name,
            product_price=product.price
        ))
    return detailed