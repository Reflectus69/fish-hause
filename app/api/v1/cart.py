from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import cart_service
from app.models import cart as cart_schemas
from app.models import user as user_schemas
from app.core.security import get_current_user

router = APIRouter()

@router.get("", response_model=cart_schemas.Cart)
def read_user_cart(db: Session = Depends(get_db), current_user: user_schemas.Customer = Depends(get_current_user)):
    """
    Retrieve the current user's cart.
    """
    cart = cart_service.get_active_cart_by_customer_id(db, customer_id=current_user.id)
    return cart

@router.post("/items", response_model=cart_schemas.CartItem)
def add_item_to_cart(
    item: cart_schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: user_schemas.Customer = Depends(get_current_user)
):
    """
    Add an item to the current user's cart.
    """
    cart = cart_service.get_active_cart_by_customer_id(db, customer_id=current_user.id)
    return cart_service.add_item_to_cart(db, cart_id=cart.id, item=item)

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: user_schemas.Customer = Depends(get_current_user)
):
    """
    Remove an item from the current user's cart.
    """
    cart = cart_service.get_active_cart_by_customer_id(db, customer_id=current_user.id)
    item = cart_service.remove_item_from_cart(db, cart_id=cart.id, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    return None
