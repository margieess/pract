from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from .. import schemas, crud
from ..dependencies import get_db, require_role

router = APIRouter(
    prefix="/invoices",
    tags=["invoices"],
)

@router.post("/", response_model=schemas.Invoice)
def create_invoice(
    invoice: schemas.InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(require_role("cashier"))
):
    db_invoice = crud.create_invoice(db=db, invoice=invoice)
    if not db_invoice:
        raise HTTPException(status_code=400, detail="Order not found or not processed")
    return db_invoice



@router.get("/", response_model=List[schemas.Invoice])
def read_invoices(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(require_role("accountant"))
):
    return crud.get_invoices(db=db, skip=skip, limit=limit, start_date=start_date, end_date=end_date)

