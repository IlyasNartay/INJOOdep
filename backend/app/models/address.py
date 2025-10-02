from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    address = Column(String, nullable=False)       # полный адрес, например "137, ул. Абая"
    apartment = Column(String, nullable=True)      # квартира
    entrance = Column(String, nullable=True)       # подъезд
    floor = Column(String, nullable=True)          # этаж

    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="address", cascade="all, delete-orphan")

    def full_address(self) -> str:
        parts = [self.address]
        if self.entrance:
            parts.append(f"подъезд {self.entrance}")
        if self.floor:
            parts.append(f"этаж {self.floor}")
        if self.apartment:
            parts.append(f"кв.{self.apartment}")
        return ", ".join(parts)
