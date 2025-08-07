from sqlalchemy.orm import Session, joinedload
from datetime import datetime
import uuid

from app.db import models as db_models
from app.services import cart_service

def create_order_from_cart(db: Session, customer_id: int):
    """
    Creates an order for a customer from their active cart.
    """
    # 1. Get the user's cart
    cart = cart_service.get_active_cart_by_customer_id(db, customer_id)
    if not cart or not cart.items:
        return None # Or raise an exception

    # 2. Create the Order record
    total_amount = 0
    order_items_to_create = []

    for item in cart.items:
        # NOTE: In a real app, get price from a pricelist or product variant table
        unit_price = 10.0
        total_amount += item.qty_units * unit_price
        order_items_to_create.append(
            db_models.OrderItem(
                product_variant_id=item.product_variant_id,
                qty_units=item.qty_units,
                unit_price=unit_price,
            )
        )

    new_order = db_models.Order(
        order_no=str(uuid.uuid4()),
        customer_id=customer_id,
        status="pending",
        created_at=datetime.utcnow(),
        total_amount=total_amount,
        items=order_items_to_create
    )

    db.add(new_order)

    # 3. Clear the cart
    for item in cart.items:
        db.delete(item)

    cart.updated_at = datetime.utcnow()
    db.add(cart)

    db.commit()
    db.refresh(new_order)

    return new_order

def get_orders_by_customer(db: Session, customer_id: int):
    """
    Get all orders for a specific customer.
    """
    return db.query(db_models.Order).filter(db_models.Order.customer_id == customer_id).all()
