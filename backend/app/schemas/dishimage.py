from pydantic import BaseModel
from typing import Optional

class DishImageBase(BaseModel):
    image_url: str

    model_config = {
        "from_attributes": True
    }

class DishImageCreate(DishImageBase):
    pass


class DishImageRead(BaseModel):
    id: int
    image_url: str

    model_config = {
        "from_attributes": True
    }