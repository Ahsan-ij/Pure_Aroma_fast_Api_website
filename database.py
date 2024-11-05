import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, Product,CartItem



DATABASE_URL = "postgresql://postgres:Ahsan@localhost:5432/my_product"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

with open('C:/Users/Ahsan/Documents/Fast_Api_Website/Pure_Aroma/product.json') as f:
    data = json.load(f)
    session = SessionLocal()

    for category, products in data.items():
        if isinstance(products, list):
            for product in products:  
                if isinstance(product, dict):  
                    existing_product = session.query(Product).filter_by(id=product['id']).first()
                    if existing_product is None:
                        new_product = Product(
                            id=product['id'],
                            name=product['name'],
                            image_url=product['image_url'],
                            price=product['price'],
                            section=category
                            )
                        session.add(new_product)
                    else:
                        print(f"Product with ID {product['id']} already exists. Skipping.")

    
# Commit the session
# try:
#     session.commit()
#     print("Data added successfully!")
# except IntegrityError as e:
#     session.rollback()
#     print(f"Integrity error occurred: {e.orig}")
# except Exception as e:
#     session.rollback()
#     print(f"An error occurred: {e}")
# finally:
#     session.close()

# Fetch and display all products from the database
session = SessionLocal()
stored_products = session.query(Product).all()

# if stored_products:
#     print("Products in the database:")
#     for p in stored_products:
#         print(f"ID: {p.id}, Name: {p.name}, Price: {p.price}, Section: {p.section}")
# else:
#     print("No products found in the database.")

session.close()


