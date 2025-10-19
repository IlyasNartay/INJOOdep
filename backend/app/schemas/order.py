from pydantic import BaseModel
from typing import List
from .dish import DishRead

class DishInOrder(BaseModel):
    dish_id: int
    quantity: int

class OrderCreate(BaseModel):
    address_id: int
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
    status: str
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
