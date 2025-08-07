from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Customer/User Schemas ---
class CustomerBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None

class CustomerCreate(CustomerBase):
    password: str

class Customer(CustomerBase):
    id: int
    is_wholesale: bool

    class Config:
        orm_mode = True
