from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.deps import get_db
from app import schemas, services
from app.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=schemas.OrderRead)
async def create_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await services.create_order(db, order_data,current_user)
@router.get("/my", response_model=List[schemas.OrderRead])
def get_order(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return services.get_my_orders(db, current_user)
@router.post("/table")
async def create_table_order(
    order: schemas.TableOrderCreate,
    db: Session = Depends(get_db)
):
    db_order =  await services.create_table_order(order, db)
    return {"message": "Order created", "order_id": db_order.id}