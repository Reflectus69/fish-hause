from fastapi import FastAPI
from app.api.v1 import products as products_router
from app.api.v1 import auth as auth_router
from app.api.v1 import cart as cart_router
from app.api.v1 import categories as categories_router
from app.api.v1 import orders as orders_router

app = FastAPI(
    title="E-commerce Store API",
    description="API for the online store, based on the provided database schema.",
    version="1.0.0",
)

# Include the API routers
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(products_router.router, prefix="/api/v1/products", tags=["products"])
app.include_router(cart_router.router, prefix="/api/v1/cart", tags=["cart"])
app.include_router(categories_router.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(orders_router.router, prefix="/api/v1/orders", tags=["orders"])


@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce Store API!"}
