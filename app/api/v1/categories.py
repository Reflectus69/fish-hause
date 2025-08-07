from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import product_service
from app.models import product as product_schemas

router = APIRouter()

@router.get("/", response_model=List[product_schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of categories.
    """
    categories = product_service.get_categories(db, skip=skip, limit=limit)
    return categories
