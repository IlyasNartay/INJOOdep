from sqlalchemy.orm import Session
from app.models.address import Address
from app.schemas.address import AddressCreate

def create_address(db: Session, user_id: int, data: AddressCreate):
    addr = Address(**data.dict(), user_id=user_id)
    db.add(addr)
    db.commit()
    db.refresh(addr)
    return addr

def get_user_addresses(db: Session, user_id: int):
    return db.query(Address).filter(Address.user_id == user_id).all()


def delete_address(db: Session, user_id: int, address_id: int):
    address = db.query(Address).filter(Address.id == address_id, Address.user_id == user_id).first()
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Адрес не найден или не принадлежит вам"
        )
    db.delete(address)
    db.commit()
    return {"detail": "Адрес удалён"}