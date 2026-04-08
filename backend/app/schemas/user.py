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
    status: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user_role: UserRole
    user_status: str


class TokenData(BaseModel):
    phone: Optional[str] = None


class LoginRequest(BaseModel):
    phone: str
    password: str


class RoleOption(BaseModel):
    key: UserRole
    label: str


class StatusOption(BaseModel):
    key: str
    label: str


class AuthMetaResponse(BaseModel):
    roles: list[RoleOption]
    statuses: list[StatusOption]
    guest_mode: str = "guest"
