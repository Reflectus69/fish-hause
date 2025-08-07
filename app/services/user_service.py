from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.db import models as db_models
from app.models import user as user_schemas

def get_user_by_email(db: Session, email: str):
    """
    Get a single user by email.
    """
    return db.query(db_models.Customer).filter(db_models.Customer.email == email).first()

def create_user(db: Session, user: user_schemas.CustomerCreate):
    """
    Create a new user.
    """
    hashed_password = get_password_hash(user.password)
    db_user = db_models.Customer(
        email=user.email,
        name=user.name,
        phone=user.phone,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
