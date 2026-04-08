from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.order import Order, OrderDish
from app.models.tguser import TelegramUser
from app.models.user import User, UserRole, UserStatus
from app.schemas.admin_users import (
    AdminTelegramUserListItem,
    AdminTelegramUserListResponse,
    AdminUserDetail,
    AdminUserListItem,
    AdminUserListResponse,
    AdminUserStats,
)
from app.schemas.order import OrderRead

TG_USER_ROLES = {"admin", "kitchen", "courier"}


def get_tg_users(db: Session) -> AdminTelegramUserListResponse:
    rows = (
        db.query(TelegramUser)
        .order_by(TelegramUser.created_at.desc().nullslast(), TelegramUser.id.desc())
        .all()
    )

    return AdminTelegramUserListResponse(
        items=[
            AdminTelegramUserListItem(
                id=item.id,
                chat_id=item.chat_id,
                role=item.role,
                created_at=item.created_at,
            )
            for item in rows
        ],
        total=len(rows),
    )


def set_tg_user_role(db: Session, tg_user_id: int, role: str) -> TelegramUser:
    normalized_role = (role or "").strip().lower()
    if normalized_role not in TG_USER_ROLES:
        raise HTTPException(status_code=400, detail="Invalid telegram role")

    user = db.query(TelegramUser).filter(TelegramUser.id == tg_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Telegram user not found")

    user.role = normalized_role
    db.commit()
    db.refresh(user)
    return user


def delete_tg_user(db: Session, tg_user_id: int) -> None:
    user = db.query(TelegramUser).filter(TelegramUser.id == tg_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Telegram user not found")

    db.delete(user)
    db.commit()
def _normalize_user_status(value: str | None) -> str:
    return value or UserStatus.active.value


def get_users(
    db: Session,
    search: str | None = None,
    role: UserRole | None = None,
    status: UserStatus | None = None,
    page: int = 1,
    limit: int = 10,
) -> AdminUserListResponse:
    query = (
        db.query(
            User,
            func.count(Order.id).label("orders_count"),
            func.coalesce(func.sum(Order.total_price), 0).label("total_spent"),
            func.max(Order.rate_at).label("last_order_at"),
        )
        .outerjoin(Order, Order.user_id == User.id)
        .group_by(User.id)
    )

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            (User.phone.ilike(term)) | (User.full_name.ilike(term))
        )

    if role:
        query = query.filter(User.role == role)

    if status:
        query = query.filter(func.coalesce(User.status, UserStatus.active.value) == status.value)

    total = db.query(func.count()).select_from(query.subquery()).scalar() or 0
    pages = max(1, (total + limit - 1) // limit)
    page = max(1, min(page, pages))

    rows = (
        query.order_by(User.created_at.desc().nullslast(), User.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    items = [
        AdminUserListItem(
            id=user.id,
            phone=user.phone,
            full_name=user.full_name,
            role=user.role,
            status=_normalize_user_status(user.status),
            created_at=user.created_at,
            orders_count=int(orders_count or 0),
            total_spent=float(total_spent or 0),
            last_order_at=last_order_at,
        )
        for user, orders_count, total_spent, last_order_at in rows
    ]

    return AdminUserListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages,
    )


def get_user_detail(db: Session, user_id: int) -> AdminUserDetail:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    orders = (
        db.query(Order)
        .options(
            joinedload(Order.order_dishes).joinedload(OrderDish.dish)
        )
        .filter(Order.user_id == user_id)
        .order_by(Order.rate_at.desc())
        .all()
    )

    total_orders = len(orders)
    total_spent = float(sum(order.total_price for order in orders))
    avg_check = round(total_spent / total_orders, 2) if total_orders else 0.0
    last_order_at = orders[0].rate_at if orders else None

    return AdminUserDetail(
        id=user.id,
        phone=user.phone,
        full_name=user.full_name,
        role=user.role,
        status=_normalize_user_status(user.status),
        created_at=user.created_at,
        orders_count=total_orders,
        total_spent=total_spent,
        stats=AdminUserStats(
            total_orders=total_orders,
            total_spent=total_spent,
            avg_check=avg_check,
            last_order_at=last_order_at,
        ),
        orders=[OrderRead.model_validate(order, from_attributes=True) for order in orders],
    )


def set_user_status(db: Session, user_id: int, status: UserStatus) -> User:
    if status not in {UserStatus.active, UserStatus.blocked}:
        raise HTTPException(status_code=400, detail="Invalid status")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.status = status.value
    db.commit()
    db.refresh(user)
    return user


def set_user_role(db: Session, user_id: int, role: UserRole) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role
    db.commit()
    db.refresh(user)
    return user
