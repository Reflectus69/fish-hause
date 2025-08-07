from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.product import ProductVariant

# --- OrderItem Schemas ---
class OrderItemBase(BaseModel):
    product_variant_id: int
    qty_units: int
    unit_price: float

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    product_variant: ProductVariant

    class Config:
        orm_mode = True

# --- Order Schemas ---
class OrderBase(BaseModel):
    pass

class OrderCreate(OrderBase):
    # We'll create an order from a cart, so no specific payload needed here yet.
    # Could add shipping address id, etc. later.
    pass

class Order(OrderBase):
    id: int
    order_no: str
    customer_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItem] = []

    class Config:
        orm_mode = True
