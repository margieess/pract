from fastapi import FastAPI
from .routers import auth, products, orders, invoices
from .fixtures import load_fixtures
from .database import engine
from .models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

#підключення роутерів
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(invoices.router)


@app.on_event("startup")
def startup_event():
    load_fixtures()

@app.get("/")
def read_root():
    return {"message": "Tech Store API"}