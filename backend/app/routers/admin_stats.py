from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.deps import admin_required, get_db
from app.models.user import User
from app.schemas.admin_stats import AdminStatsResponse
from app.services.admin_stats_service import get_admin_stats

router = APIRouter()


@router.get("/stats", response_model=AdminStatsResponse)
def read_admin_stats(
    date_from: date | None = Query(default=None, description="Inclusive start date"),
    date_to: date | None = Query(default=None, description="Inclusive end date"),
    db: Session = Depends(get_db),
    _current_user: User = Depends(admin_required),
):
    return get_admin_stats(db=db, date_from=date_from, date_to=date_to)
