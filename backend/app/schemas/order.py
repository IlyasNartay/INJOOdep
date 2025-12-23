from pydantic import BaseModel
from typing import List, Optional
from .dish import DishRead
from datetime import datetime

class DishInOrder(BaseModel):
    dish_id: int
    quantity: int

class OrderCreate(BaseModel):
    address_id: int
    kaspi_number: str
    dishes: List[DishInOrder]

class OrderDishRead(BaseModel):
    dish: DishRead
    quantity: int

    model_config = {
        "from_attributes": True
    }

class OrderRead(BaseModel):
    id: int
    user_id: int
    address_id: int
    total_price: float
    kaspi_number: str
    status: str
    rate_at: datetime  # ✅ добавлено
    order_dishes: List[OrderDishRead]

    model_config = {
        "from_attributes": True
    }

class TableOrderRead(BaseModel):
    id: int
    table_id: int
    total_price: float
    rate_at: datetime  # ✅ добавлено
    order_dishes: List[OrderDishRead]

    model_config = {
        "from_attributes": True
    }

class TableOrderCreate(BaseModel):
    table_id: int
    dishes: List[DishInOrder]

    model_config = {
        "from_attributes": True
    }
