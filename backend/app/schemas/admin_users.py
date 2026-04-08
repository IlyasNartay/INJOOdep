from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.models.user import UserStatus
from app.schemas.order import OrderRead
from app.schemas.user import UserRole


class AdminUserListItem(BaseModel):
    id: int
    phone: str
    full_name: Optional[str] = None
    role: UserRole
    status: str
    created_at: Optional[datetime] = None
    orders_count: int
    total_spent: float
    last_order_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class AdminUserListResponse(BaseModel):
    items: List[AdminUserListItem]
    total: int
    page: int
    limit: int
    pages: int


class AdminUserStats(BaseModel):
    total_orders: int
    total_spent: float
    avg_check: float
    last_order_at: Optional[datetime] = None


class AdminUserDetail(BaseModel):
    id: int
    phone: str
    full_name: Optional[str] = None
    role: UserRole
    status: str
    created_at: Optional[datetime] = None
    orders_count: int
    total_spent: float
    stats: AdminUserStats
    orders: List[OrderRead]

    model_config = {
        "from_attributes": True
    }


class AdminUserRoleUpdate(BaseModel):
    role: UserRole


class AdminUserStatusUpdate(BaseModel):
    status: UserStatus


class AdminTelegramUserListItem(BaseModel):
    id: int
    chat_id: str
    role: str
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class AdminTelegramUserListResponse(BaseModel):
    items: List[AdminTelegramUserListItem]
    total: int


class AdminTelegramUserRoleUpdate(BaseModel):
    role: str
