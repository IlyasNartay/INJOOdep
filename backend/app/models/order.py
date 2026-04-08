from sqlalchemy import String, Text, Column, Integer, ForeignKey, DateTime, Float, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.constants.order_status import OrderStatus

class OrderDish(Base):
    __tablename__ = "order_dishes"

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True)
    dish_id = Column(Integer, ForeignKey("dishes.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)

    order = relationship("Order", back_populates="order_dishes")
    dish = relationship("Dish", back_populates="order_dishes")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id", ondelete="CASCADE"), nullable=False)

    status = Column(SqlEnum(OrderStatus), default=OrderStatus.pending, nullable=False)
    kaspi_number = Column(String, nullable=False)
    note = Column(Text, nullable=True)
    total_price = Column(Float, nullable=False)

    rate_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="orders")
    address = relationship("Address", back_populates="orders")
    order_dishes = relationship("OrderDish", back_populates="order", cascade="all, delete-orphan")

class TableOrderDish(Base):
    __tablename__ = "table_order_dishes"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("table_orders.id"))
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    quantity = Column(Integer, nullable=False)

    order = relationship("TableOrder", back_populates="dishes")
    dish = relationship("Dish", back_populates="table_order_dishes")


class TableOrder(Base):
    __tablename__ = "table_orders"

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, index=True)
    total_price = Column(Float, nullable=False)

    rate_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    dishes = relationship("TableOrderDish", back_populates="order")
