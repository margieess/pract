"""
роутер для роботи із замовленнями оrders

касир може створювати та оплачувати замовлення
консультант може опрацьовувати замовлення зі статусом created
"""

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, crud, models
from ..dependencies import get_db, get_current_active_user, require_role

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@router.post("/", response_model=schemas.Order)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(require_role("cashier"))
):
    return crud.create_order(db=db, order=order, cashier_id=current_user.id)

@router.get("/", response_model=List[schemas.Order])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    if current_user.role == "consultant":
        return db.query(models.Order).filter(models.Order.status == "created").offset(skip).limit(limit).all()
    return crud.get_orders(db=db, skip=skip, limit=limit)

@router.patch("/{order_id}/process", response_model=schemas.Order)
def process_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(require_role("consultant"))
):
    db_order = crud.process_order(db, order_id=order_id, user_id=current_user.id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found or cannot be processed")
    return db_order

@router.patch("/{order_id}/pay", response_model=schemas.Order)
def pay_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(require_role("cashier"))
):
    db_order = crud.pay_order(db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=400, detail="Order not found or not processed")
    return db_order