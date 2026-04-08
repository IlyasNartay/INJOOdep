from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.deps import admin_required, get_db
from app.models.user import User, UserRole, UserStatus
from app.schemas.admin_users import (
    AdminTelegramUserListResponse,
    AdminTelegramUserRoleUpdate,
    AdminUserDetail,
    AdminUserListResponse,
    AdminUserRoleUpdate,
    AdminUserStatusUpdate,
)
from app.services.admin_users_service import (
    delete_tg_user,
    get_tg_users,
    get_user_detail,
    get_users,
    set_tg_user_role,
    set_user_role,
    set_user_status,
)

router = APIRouter()


@router.get("/users", response_model=AdminUserListResponse)
def list_users(
    search: str | None = Query(default=None),
    role: UserRole | None = Query(default=None),
    status: UserStatus | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    _current_user: User = Depends(admin_required),
):
    return get_users(db=db, search=search, role=role, status=status, page=page, limit=limit)


@router.get("/users/{user_id}", response_model=AdminUserDetail)
def user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(admin_required),
):
    return get_user_detail(db=db, user_id=user_id)


@router.patch("/users/{user_id}/status", response_model=AdminUserDetail)
def update_user_status(
    user_id: int,
    payload: AdminUserStatusUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(admin_required),
):
    set_user_status(db=db, user_id=user_id, status=payload.status)
    return get_user_detail(db=db, user_id=user_id)


@router.patch("/users/{user_id}/role", response_model=AdminUserDetail)
def update_user_role(
    user_id: int,
    payload: AdminUserRoleUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(admin_required),
):
    set_user_role(db=db, user_id=user_id, role=payload.role)
    return get_user_detail(db=db, user_id=user_id)


@router.get("/tg-users", response_model=AdminTelegramUserListResponse)
def list_tg_users(
    db: Session = Depends(get_db),
    _current_user: User = Depends(admin_required),
):
    return get_tg_users(db=db)


@router.patch("/tg-users/{tg_user_id}/role", response_model=AdminTelegramUserListResponse)
def update_tg_user_role(
    tg_user_id: int,
    payload: AdminTelegramUserRoleUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(admin_required),
):
    set_tg_user_role(db=db, tg_user_id=tg_user_id, role=payload.role)
    return get_tg_users(db=db)


@router.delete("/tg-users/{tg_user_id}", response_model=AdminTelegramUserListResponse)
def remove_tg_user(
    tg_user_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(admin_required),
):
    delete_tg_user(db=db, tg_user_id=tg_user_id)
    return get_tg_users(db=db)
