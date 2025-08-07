from pydantic import BaseModel
from typing import List, Optional

# Pydantic models (schemas) for data validation and response models

# --- Category Schemas ---
class CategoryBase(BaseModel):
    name_ru: str
    slug: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True

# --- ProductVariant Schemas ---
class ProductVariantBase(BaseModel):
    sku: str
    name: str
    weight_type: Optional[str] = None
    unit: Optional[str] = None

class ProductVariantCreate(ProductVariantBase):
    pass

class ProductVariant(ProductVariantBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True

# --- Product Schemas ---
class ProductBase(BaseModel):
    sku_root: str
    name_ru: str
    description: Optional[str] = None
    is_active: bool = True

class ProductCreate(ProductBase):
    category_id: int

class Product(ProductBase):
    id: int
    category_id: int
    variants: List[ProductVariant] = []

    class Config:
        orm_mode = True
