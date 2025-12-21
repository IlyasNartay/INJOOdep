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
    available: bool = True


class DishCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = ""
    category: Optional[str] = ""
    available: Optional[bool] = True   # можно не передавать


class DishUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    available: Optional[bool] = None   # важно для disable/enable


class DishRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    category: Optional[str]
    available: bool
    images: Optional[List[DishImageRead]] = None

    model_config = {
        "from_attributes": True
    }
