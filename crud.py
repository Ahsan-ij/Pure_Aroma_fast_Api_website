from sqlalchemy.orm import Session
from models import Product

def search_products_by_name(db: Session, query: str, limit: int = 20, offset: int = 0):
    
    results = db.query(Product).filter(Product.name.ilike(f"%{query}%")) \
        .limit(limit).offset(offset).all()
    return results

def get_all_products(db: Session):
    return db.query(Product).all()

def get_products_by_gender(db: Session, section: str):
    return db.query(Product).filter(Product.section == section).all()
