from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from app.database import Base
from sqlalchemy.orm import relationship

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    available = Column(Boolean, nullable=False, default=True)
    images = relationship("DishImage", back_populates="dish", cascade="all, delete")
    category = Column(String, nullable=True)

    order_dishes = relationship("OrderDish", back_populates="dish", cascade="all, delete-orphan")
    table_order_dishes = relationship("TableOrderDish", back_populates="dish")
