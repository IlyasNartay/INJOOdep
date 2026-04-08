import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String, text
from sqlalchemy.orm import relationship

from app.database import Base

class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"
    customer = "customer"


class UserStatus(str, enum.Enum):
    active = "active"
    blocked = "blocked"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    phone = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.customer, nullable=False)
    status = Column(String, default=UserStatus.active.value, nullable=False, server_default=text("'active'"))
    created_at = Column(
        DateTime,
        nullable=True,
        default=datetime.utcnow,
        server_default=text("NOW()"),
    )

    addresses = relationship("Address", back_populates="user", cascade="all, delete")
    orders = relationship("Order", back_populates="user")
