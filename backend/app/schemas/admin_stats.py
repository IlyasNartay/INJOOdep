from datetime import date

from pydantic import BaseModel


class AdminOverviewMetrics(BaseModel):
    total_revenue: float
    total_orders: int
    avg_check: float
    new_users: int


class DailyRevenueItem(BaseModel):
    date: date
    revenue: float


class TopDishItem(BaseModel):
    name: str
    quantity: int
    revenue: float


class OrderStatusItem(BaseModel):
    status: str
    count: int


class AdminStatsResponse(BaseModel):
    overview: AdminOverviewMetrics
    revenue_by_day: list[DailyRevenueItem]
    top_dishes: list[TopDishItem]
    order_statuses: list[OrderStatusItem]
