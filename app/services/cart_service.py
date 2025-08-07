from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from app.db import models as db_models
from app.models import cart as cart_schemas

def get_active_cart_by_customer_id(db: Session, customer_id: int):
    """
    Retrieves the active cart for a customer. If none exists, creates one.
    """
    cart = db.query(db_models.Cart).filter(db_models.Cart.customer_id == customer_id).first()
    if not cart:
        cart = db_models.Cart(customer_id=customer_id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        db.add(cart)
        db.commit()
        db.refresh(cart)
    # Eagerly load items and their product variants
    return db.query(db_models.Cart).options(
        joinedload(db_models.Cart.items).joinedload(db_models.CartItem.product_variant)
    ).filter(db_models.Cart.id == cart.id).first()

def add_item_to_cart(db: Session, cart_id: int, item: cart_schemas.CartItemCreate):
    """
    Adds an item to a cart. If the item already exists, updates the quantity.
    """
    db_item = db.query(db_models.CartItem).filter(
        db_models.CartItem.cart_id == cart_id,
        db_models.CartItem.product_variant_id == item.product_variant_id
    ).first()

    if db_item:
        db_item.qty_units += item.qty_units
    else:
        db_item = db_models.CartItem(**item.dict(), cart_id=cart_id)
        db.add(db_item)

    db.query(db_models.Cart).filter(db_models.Cart.id == cart_id).update({"updated_at": datetime.utcnow()})
    db.commit()
    db.refresh(db_item)
    return db_item

def remove_item_from_cart(db: Session, cart_id: int, item_id: int):
    """
    Removes an item from a cart.
    """
    db_item = db.query(db_models.CartItem).filter(
        db_models.CartItem.id == item_id,
        db_models.CartItem.cart_id == cart_id
    ).first()

    if db_item:
        db.delete(db_item)
        db.query(db_models.Cart).filter(db_models.Cart.id == cart_id).update({"updated_at": datetime.utcnow()})
        db.commit()

    return db_item
