from pydantic import BaseModel
from typing import List
from .dish import DishRead

class DishInOrder(BaseModel):
    dish_id: int
    quantity: int

class OrderCreate(BaseModel):
    address_id: int
    kaspi_number: str
    dishes: List[DishInOrder]

class OrderDishRead(BaseModel):
    dish: DishRead
    kaspi_number: str
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
    order_dishes: List[OrderDishRead]

    model_config = {
        "from_attributes": True
    }

class TableOrderRead(BaseModel):
    id: int
    table_id: int
    total_price: float
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
