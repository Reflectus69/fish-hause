from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import order_service
from app.models import order as order_schemas
from app.models import user as user_schemas
from app.core.security import get_current_user

router = APIRouter()

@router.post("", response_model=order_schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(
    db: Session = Depends(get_db),
    current_user: user_schemas.Customer = Depends(get_current_user)
):
    """
    Create an order from the current user's cart.
    """
    order = order_service.create_order_from_cart(db, customer_id=current_user.id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty or does not exist.",
        )
    return order

@router.get("", response_model=List[order_schemas.Order])
def list_user_orders(
    db: Session = Depends(get_db),
    current_user: user_schemas.Customer = Depends(get_current_user)
):
    """
    List all orders for the current user.
    """
    orders = order_service.get_orders_by_customer(db, customer_id=current_user.id)
    return orders
