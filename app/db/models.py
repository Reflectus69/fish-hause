from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text,
    DateTime,
    Numeric
)
from sqlalchemy.orm import relationship
from .base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id"))
    name_ru = Column(String)
    slug = Column(String, unique=True, index=True)

    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku_root = Column(String, unique=True, index=True)
    name_ru = Column(String)
    name_en = Column(String)
    latin_name = Column(String)
    species = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    description = Column(Text)
    origin_region = Column(String)
    lake = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)

    category = relationship("Category", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product")
    attributes = relationship("ProductAttribute", uselist=False, back_populates="product")
    media = relationship("ProductMedia", back_populates="product")

class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    sku = Column(String, unique=True, index=True)
    name = Column(String)
    weight_type = Column(String)
    weight_min = Column(Numeric)
    weight_max = Column(Numeric)
    net_weight_avg = Column(Numeric)
    unit = Column(String)

    product = relationship("Product", back_populates="variants")

class ProductAttribute(Base):
    __tablename__ = "product_attributes"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True)
    fat_content = Column(Numeric)
    boneiness_level = Column(String)
    cut_type = Column(String)
    is_wild = Column(Boolean)
    is_introduced = Column(Boolean)
    shelf_life_days = Column(Integer)
    storage_temp_c_from = Column(Numeric)
    storage_temp_c_to = Column(Numeric)
    restricted_until = Column(DateTime)

    product = relationship("Product", back_populates="attributes")

class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    url = Column(String)
    storage = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    duration_sec = Column(Integer)
    created_at = Column(DateTime)

class ProductMedia(Base):
    __tablename__ = "product_media"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    media_id = Column(Integer, ForeignKey("media.id"))
    purpose = Column(String)
    channel_id = Column(Integer, ForeignKey("channels.id")) # Note: channels table not defined yet
    sort_order = Column(Integer)
    caption = Column(String)

    product = relationship("Product", back_populates="media")
    media = relationship("Media")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False) # Essential for security
    region_id = Column(Integer, ForeignKey("regions.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))
    address = Column(Text)
    is_wholesale = Column(Boolean, default=False)
    notes = Column(Text)

    carts = relationship("Cart", back_populates="customer")

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    customer = relationship("Customer", back_populates="carts")
    items = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_variant_id = Column(Integer, ForeignKey("product_variants.id"))
    qty_units = Column(Integer)
    # For simplicity, focusing on qty_units. qty_kg can be added later.

    cart = relationship("Cart", back_populates="items")
    product_variant = relationship("ProductVariant")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String, unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(String, default="pending")
    created_at = Column(DateTime)
    total_amount = Column(Numeric)

    customer = relationship("Customer")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_variant_id = Column(Integer, ForeignKey("product_variants.id"))
    qty_units = Column(Integer)
    unit_price = Column(Numeric)

    order = relationship("Order", back_populates="items")
    product_variant = relationship("ProductVariant")


# We will need to define other models like Channel later
class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)

class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)

class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"))
    name = Column(String)
    code = Column(String)
