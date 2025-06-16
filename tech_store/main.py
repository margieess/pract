from fastapi import FastAPI
from .database import engine
from . import models
from .routers import auth, products, orders, invoices
from .fixtures import load_fixtures  # <-- імпортуємо


# Створення таблиць у базі даних (якщо їх ще немає)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Підключення роутерів
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(invoices.router)

@app.on_event("startup")
def startup_event():
    load_fixtures()  # <-- викликаємо при старті сервера

@app.get("/")
def read_root():
    return {"message": "Tech Store API"}

