# app/models.py
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, text

from app.database import Base

class TelegramUser(Base):
    __tablename__ = "telegram_users"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, unique=True, index=True)
    role = Column(String)  # "kitchen" или "courier"
    created_at = Column(
        DateTime,
        nullable=True,
        default=datetime.utcnow,
        server_default=text("NOW()"),
    )
