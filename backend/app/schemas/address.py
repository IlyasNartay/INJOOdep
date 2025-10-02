from pydantic import BaseModel
from typing import Optional

class AddressBase(BaseModel):
    address: str                      # полный адрес (например: "137, ул. Абая")
    apartment: Optional[str] = None   # квартира
    entrance: Optional[str] = None    # подъезд
    floor: Optional[str] = None       # этаж

class AddressCreate(AddressBase):
    pass

class AddressOut(AddressBase):
    id: int

    model_config = {
        "from_attributes": True
    }
