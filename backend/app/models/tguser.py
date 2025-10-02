# app/models.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class TelegramUser(Base):
    __tablename__ = "telegram_users"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, unique=True, index=True)
    role = Column(String)  # "kitchen" или "courier"
