from sqlalchemy.orm import Session
from .models import Brand, Category, Product
from project.loggs.logger_config import logger 

# -------- GETTER Functions --------

def get_brands(db: Session):
    logger.debug("Fetching all brands from database.")
    return db.query(Brand).all()

def count_products_for_brand(db: Session, brand_name: str):
    logger.debug(f"Counting products for brand: {brand_name}")
    brand = db.query(Brand).filter(Brand.name == brand_name).first()
    if not brand:
        logger.warning(f"No brand found with name: {brand_name}")
        return 0
    count = db.query(Product).filter(Product.brand_id == brand.id).count()
    logger.info(f"Found {count} products for brand: {brand_name}")
    return count

def filter_products_by_price(db: Session, min_price: float = 0, max_price: float = 100000):
    logger.debug(f"Filtering products with price between {min_price} and {max_price}")
    return db.query(Product).filter(Product.price >= min_price, Product.price <= max_price).all()

# -------- CREATE / UPSERT Functions --------

def get_or_create_brand(db: Session, brand_name: str):
    brand_name = brand_name or "Unknown"
    brand = db.query(Brand).filter_by(name=brand_name).first()
    if not brand:
        logger.info(f"Creating new brand: {brand_name}")
        brand = Brand(name=brand_name)
        db.add(brand)
        db.commit()
        db.refresh(brand)
    else:
        logger.debug(f"Brand already exists: {brand_name}")
    return brand

def get_or_create_category(db: Session, category_name: str, category_url: str):
    category_name = category_name or "Unknown"
    category = db.query(Category).filter_by(name=category_name).first()
    if not category:
        logger.info(f"Creating new category: {category_name} (URL: {category_url})")
        category = Category(name=category_name, url=category_url)
        db.add(category)
        db.commit()
        db.refresh(category)
    else:
        logger.debug(f"Category already exists: {category_name}")
    return category

def insert_product(db: Session, product_dict):
    logger.debug(f"Inserting product: {product_dict.get('Product Name', '')}")
    
    brand = get_or_create_brand(db, product_dict.get("Brand", "Unknown"))
    
    category_name = product_dict["Category Name"]
    category_url = product_dict["Category URL"]
    category = get_or_create_category(db, category_name, category_url)

    existing = db.query(Product).filter(Product.url == product_dict["Product URL"]).first()
    if existing:
        logger.warning(f"⚠️ Product already exists: {product_dict['Product URL']}")
        return

    new_product = Product(
        brand_id=brand.id,
        category_id=category.id,
        product_id=product_dict["Product ID"],
        title=product_dict["Product Name"],
        url=product_dict["Product URL"],
        image_urls=product_dict["Image URL"],
        price=float(product_dict["Price"]) if product_dict["Price"] else None,
        discounted_price=float(product_dict["Discounted Price"]) if product_dict["Discounted Price"] else None,
    )

    db.add(new_product)
    db.commit()
    logger.info(f"✅ Inserted product: {new_product.title}")
