from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.schemas.address import AddressCreate, AddressOut
from app.services import address_service

router = APIRouter()

@router.post("/", response_model=AddressOut)
def add_address(data: AddressCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return address_service.create_address(db, user.id, data)

@router.get("/", response_model=list[AddressOut])
def get_my_addresses(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return address_service.get_user_addresses(db, user.id)

@router.delete("/{address_id}")
def delete_my_address(
    address_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return address_service.delete_address(db, user.id, address_id)