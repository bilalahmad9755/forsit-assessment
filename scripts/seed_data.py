from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from app.db.session import SessionLocal
from app.models.models import Category, Product, Inventory, Sale, ChangeType

def seed_data():
    db = SessionLocal()
    try:
        
        categories = [
            Category(name="Electronics", description="Electronic devices and accessories"),
            Category(name="Clothing", description="Apparel and fashion items"),
            Category(name="Books", description="Books and publications"),
            Category(name="Home & Kitchen", description="Home and kitchen appliances"),
            Category(name="Sports", description="Sports equipment and accessories")
        ]
        for category in categories:
            db.add(category)
        db.commit()

        
        products = []
        for category in categories:
            for i in range(5):  
                product = Product(
                    name=f"{category.name} Product {i+1}",
                    description=f"Description for {category.name} Product {i+1}",
                    price=round(random.uniform(10.0, 1000.0), 2),
                    category_id=category.id
                )
                products.append(product)
                db.add(product)
        db.commit()

        
        for product in products:
            inventory = Inventory(
                product_id=product.id,
                quantity=random.randint(0, 100),
                low_stock_threshold=10
            )
            db.add(inventory)
        db.commit()

        
        for product in products:
            
            for i in range(30):
                sale_date = datetime.utcnow() - timedelta(days=i)
                quantity = random.randint(1, 5)
                sale = Sale(
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.price,
                    total_amount=quantity * product.price,
                    sale_date=sale_date
                )
                db.add(sale)
        db.commit()

        print("Sample data created successfully!")

    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data() 