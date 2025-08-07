from pydantic import BaseModel
from typing import List, Optional
from app.models.product import ProductVariant # Re-use product variant schema

# --- CartItem Schemas ---
class CartItemBase(BaseModel):
    product_variant_id: int
    qty_units: int

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    cart_id: int
    product_variant: ProductVariant

    class Config:
        orm_mode = True

# --- Cart Schemas ---
class CartBase(BaseModel):
    pass

class Cart(CartBase):
    id: int
    customer_id: int
    items: List[CartItem] = []

    class Config:
        orm_mode = True
