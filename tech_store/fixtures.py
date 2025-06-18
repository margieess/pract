from .database import SessionLocal
from .models import Product, User
from datetime import datetime, timezone, timedelta

def load_fixtures():
    db = SessionLocal()

   
    if not db.query(Product).first():
        products = [
            Product(
                name="Laptop ASUS TUF Gaming F15 FX507ZC4-HN083",
                price=32.999,
                created_at=datetime.now(timezone.utc) - timedelta(days=40) 
            ),
            Product(
                name="Smartphone Samsung Galaxy A36 5G 8/256GB Awesome Black",
                price=14.799,
                created_at=datetime.now(timezone.utc) 
            ),
            Product(
                name="Tablet Samsung Galaxy Tab A9 Plus Wi-Fi 8/128GB Graphite",
                price=8.559,
                created_at=datetime.now(timezone.utc)
            ),
            Product(
                name="Laptop ASUS Vivobook 16X K3605ZF-RP567",
                price=27.999,
                created_at=datetime.now(timezone.utc)
            ),
            Product(
                name="Smartphone Xiaomi Redmi Note 14 8/256GB Midnight Black",
                price=7.499,
                created_at=datetime.now(timezone.utc)
            ),
            Product(
                name="Tablet Lenovo Tab M11 Wi-Fi 4/128GB Seafoam Green",
                price=5.999,
                created_at=datetime.now(timezone.utc)
            )
        ]
        db.add_all(products)
        db.commit()

    if not db.query(User).first():
        users = [
            {"username": "Rita", "password": "12345", "role": "cashier"},
            {"username": "Magie", "password": "1234", "role": "consultant"},
            {"username": "Margo", "password": "1234", "role": "accountant"},
        ]
        for u in users:
            user = User(
                username=u["username"],
                password=u["password"],  
                role=u["role"]
            )
            db.add(user)
        db.commit()

    db.close()