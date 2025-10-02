# app/models/dish_image.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class DishImage(Base):
    __tablename__ = "dish_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    dish_id = Column(Integer, ForeignKey("dishes.id", ondelete="CASCADE"))

    dish = relationship("Dish", back_populates="images")
