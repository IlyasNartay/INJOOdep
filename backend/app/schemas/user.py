from pydantic import BaseModel
from typing import Optional
from app.models.user import UserRole


class UserBase(BaseModel):
    phone: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user_role: UserRole


class TokenData(BaseModel):
    phone: Optional[str] = None


class LoginRequest(BaseModel):
    phone: str
    password: str
