from sqlalchemy.orm import Session
from .models import Brand, Product

def get_brands(db: Session):
    return db.query(Brand).all()

def count_products_for_brand(db: Session, brand_name: str):
    brand = db.query(Brand).filter(Brand.name == brand_name).first()
    if not brand:
        return 0
    return db.query(Product).filter(Product.brand_id == brand.id).count()

def filter_products_by_price(db: Session, min_price: float = 0, max_price: float = 100000):
    return db.query(Product).filter(Product.price >= min_price, Product.price <= max_price).all()
