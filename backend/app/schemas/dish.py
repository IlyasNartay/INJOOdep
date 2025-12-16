# app/schemas/dish.py

from pydantic import BaseModel
from typing import List, Optional


class DishImageBase(BaseModel):
    image_url: str

    model_config = {
        "from_attributes": True
    }


class DishImageRead(DishImageBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class DishBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None


class DishCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = ""
    category: Optional[str] = ""

class DishUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None


class DishRead(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    images: Optional[List[DishImageRead]] = None

    model_config = {
        "from_attributes": True
    }