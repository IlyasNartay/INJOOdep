from datetime import date, datetime, time, timedelta

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Query, Session

from app.models.dish import Dish
from app.models.order import Order, OrderDish
from app.models.tguser import TelegramUser
from app.models.user import User
from app.schemas.admin_stats import (
    AdminOverviewMetrics,
    AdminStatsResponse,
    DailyRevenueItem,
    OrderStatusItem,
    TopDishItem,
)


def _build_date_range(
    date_from: date | None,
    date_to: date | None,
) -> tuple[datetime | None, datetime | None]:
    if date_from and date_to and date_from > date_to:
        raise HTTPException(
            status_code=400,
            detail="date_from must be earlier than or equal to date_to",
        )

    start_at = datetime.combine(date_from, time.min) if date_from else None
    end_at = datetime.combine(date_to + timedelta(days=1), time.min) if date_to else None
    return start_at, end_at


def _apply_range(
    query: Query,
    column,
    start_at: datetime | None,
    end_at: datetime | None,
) -> Query:
    if start_at is not None:
        query = query.filter(column >= start_at)
    if end_at is not None:
        query = query.filter(column < end_at)
    return query


def _to_float(value) -> float:
    return round(float(value or 0), 2)


def _normalize_order_status(value) -> str:
    return value.value if hasattr(value, "value") else str(value)


def get_admin_stats(
    db: Session,
    date_from: date | None = None,
    date_to: date | None = None,
) -> AdminStatsResponse:
    start_at, end_at = _build_date_range(date_from, date_to)

    overview_query = db.query(
        func.coalesce(func.sum(Order.total_price), 0).label("total_revenue"),
        func.count(Order.id).label("total_orders"),
        func.coalesce(func.avg(Order.total_price), 0).label("avg_check"),
    )
    overview_query = _apply_range(overview_query, Order.rate_at, start_at, end_at)
    overview_row = overview_query.one()

    user_count_query = db.query(func.count(User.id))
    tg_user_count_query = db.query(func.count(TelegramUser.id))

    if start_at is not None or end_at is not None:
        user_count_query = _apply_range(user_count_query, User.created_at, start_at, end_at)
        tg_user_count_query = _apply_range(
            tg_user_count_query,
            TelegramUser.created_at,
            start_at,
            end_at,
        )

    overview = AdminOverviewMetrics(
        total_revenue=_to_float(overview_row.total_revenue),
        total_orders=int(overview_row.total_orders or 0),
        avg_check=_to_float(overview_row.avg_check),
        new_users=int((user_count_query.scalar() or 0) + (tg_user_count_query.scalar() or 0)),
    )

    revenue_by_day_query = db.query(
        func.date(Order.rate_at).label("date"),
        func.coalesce(func.sum(Order.total_price), 0).label("revenue"),
    )
    revenue_by_day_query = _apply_range(revenue_by_day_query, Order.rate_at, start_at, end_at)
    revenue_by_day_rows = (
        revenue_by_day_query
        .group_by(func.date(Order.rate_at))
        .order_by(func.date(Order.rate_at))
        .all()
    )

    top_dishes_query = db.query(
        Dish.name.label("name"),
        func.coalesce(func.sum(OrderDish.quantity), 0).label("quantity"),
        func.coalesce(func.sum(OrderDish.quantity * Dish.price), 0).label("revenue"),
    )
    top_dishes_query = (
        top_dishes_query
        .join(OrderDish, OrderDish.dish_id == Dish.id)
        .join(Order, OrderDish.order_id == Order.id)
    )
    top_dishes_query = _apply_range(top_dishes_query, Order.rate_at, start_at, end_at)
    top_dishes_rows = (
        top_dishes_query
        .group_by(Dish.id, Dish.name)
        .order_by(
            func.sum(OrderDish.quantity).desc(),
            func.sum(OrderDish.quantity * Dish.price).desc(),
        )
        .limit(5)
        .all()
    )

    order_status_query = db.query(
        Order.status.label("status"),
        func.count(Order.id).label("count"),
    )
    order_status_query = _apply_range(order_status_query, Order.rate_at, start_at, end_at)
    order_status_rows = (
        order_status_query
        .group_by(Order.status)
        .order_by(func.count(Order.id).desc())
        .all()
    )

    return AdminStatsResponse(
        overview=overview,
        revenue_by_day=[
            DailyRevenueItem(date=row.date, revenue=_to_float(row.revenue))
            for row in revenue_by_day_rows
        ],
        top_dishes=[
            TopDishItem(
                name=row.name,
                quantity=int(row.quantity or 0),
                revenue=_to_float(row.revenue),
            )
            for row in top_dishes_rows
        ],
        order_statuses=[
            OrderStatusItem(
                status=_normalize_order_status(row.status),
                count=int(row.count or 0),
            )
            for row in order_status_rows
        ],
    )
