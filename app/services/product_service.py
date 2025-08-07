from sqlalchemy.orm import Session, joinedload
from app.db import models as db_models
from app.models import product as product_schemas

def get_product(db: Session, product_id: int):
    """
    Get a single product by ID, with its variants.
    """
    return db.query(db_models.Product).options(joinedload(db_models.Product.variants)).filter(db_models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of products.
    """
    return db.query(db_models.Product).offset(skip).limit(limit).all()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of categories.
    """
    return db.query(db_models.Category).offset(skip).limit(limit).all()
