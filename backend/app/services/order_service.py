# app/services/order_service.py
from pandas.plotting import table
from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, Depends
import asyncio
from telegram_bot.handlers import send_order_to_kitchen
from app.deps import get_current_user

async def create_order(db: Session, order_data: schemas.OrderCreate, user: models.User) -> schemas.OrderRead:
    dish_ids = [item.dish_id for item in order_data.dishes]
    dishes = db.query(models.Dish).filter(models.Dish.id.in_(dish_ids)).all()

    if len(dishes) != len(dish_ids):
        raise HTTPException(status_code=400, detail="Некоторые блюда не найдены")

    order = models.Order(
        user_id=user.id,
        address_id=order_data.address_id,
        status=models.OrderStatus.pending,
        total_price=0
    )

    total_price = 0
    for item in order_data.dishes:
        dish = next((d for d in dishes if d.id == item.dish_id), None)
        if dish is None:
            continue

        total_price += dish.price * item.quantity

        order.order_dishes.append(models.OrderDish(
            dish=dish,
            quantity=item.quantity
        ))

    order.total_price = total_price

    db.add(order)
    db.commit()
    db.refresh(order)

    # Готовим данные для отправки в Telegram
    return_data = {
        "id": order.id,
        "user_id": order.user_id,
        "address_id": order.address_id,
        "dishes": [
            {
                "id": d.id,
                "name": d.name,
                "price": d.price,
                "quantity": next(item.quantity for item in order_data.dishes if item.dish_id == d.id)
            }
            for d in dishes
        ],
        "total_price": order.total_price,
        "status": order.status
    }

    # 🔁 ВРЕМЕННО отправляем напрямую, чтобы видеть ошибки/логи
    try:
        await send_order_to_kitchen(return_data)
    except Exception as e:
        print(f"⚠️ Ошибка при отправке в Telegram (не критично): {e}")

    return schemas.OrderRead(
        id=order.id,
        user_id=order.user_id,
        address_id=order.address_id,
        total_price=order.total_price,
        status=order.status,
        order_dishes=[
            schemas.OrderDishRead(
                dish=schemas.DishRead.model_validate(od.dish),
                quantity=od.quantity
            )
            for od in order.order_dishes
        ]
    )

async def create_table_order(order_data: schemas.TableOrderCreate, db: Session):
    dish_ids = [item.dish_id for item in order_data.dishes]
    dishes = db.query(models.Dish).filter(models.Dish.id.in_(dish_ids)).all()

    if len(dishes) != len(dish_ids):
        raise HTTPException(status_code=400, detail="Некоторые блюда не найдены")

    order = models.TableOrder(
        table_id=order_data.table_id,
        total_price=0
    )

    total_price = 0
    for item in order_data.dishes:
        dish = next((d for d in dishes if d.id == item.dish_id), None)
        if dish is None:
            continue

        total_price += dish.price * item.quantity

        order.dishes.append(models.TableOrderDish(
            dish=dish,
            quantity=item.quantity
        ))

    order.total_price = total_price

    db.add(order)
    db.commit()
    db.refresh(order)

    # Готовим данные для отправки в Telegram
    return_data = {
        "id": order.id,
        "table_id": order.table_id,
        "dishes": [
            {
                "id": d.id,
                "name": d.name,
                "price": d.price,
                "quantity": next(item.quantity for item in order_data.dishes if item.dish_id == d.id)
            }
            for d in dishes
        ],
        "total_price": order.total_price,
    }

    # 🔁 ВРЕМЕННО отправляем напрямую, чтобы видеть ошибки/логи
    try:
        await send_table_order_to_kitchen(return_data)
    except Exception as e:
        print(f"⚠️ Ошибка при отправке в Telegram (не критично): {e}")

    return schemas.TableOrderRead(
        id=order.id,
        table_id=order.address_id,
        total_price=order.total_price,
        order_dishes=[
            schemas.OrderDishRead(
                dish=schemas.DishRead.model_validate(od.dish),
                quantity=od.quantity
            )
            for od in order.order_dishes
        ]
    )


def get_order_by_id(db: Session, order_id: int) -> models.Order:
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


def update_order_status(db: Session, order_id: int, new_status: str) -> models.Order:
    order = get_order_by_id(db, order_id)
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order

def get_my_orders(
        db: Session,
        current_user: models.User = Depends(get_current_user)
):
    try:
        orders = db.query(models.Order).filter(models.Order.user_id == current_user.id).all()

        return [schemas.OrderRead.model_validate(order, from_attributes=True) for order in orders]
    except Exception as e:
        print("Ошибка при получении заказов:", e)
        raise HTTPException(status_code=500, detail=str(e))
from sqlalchemy.orm import Session
from app import models, schemas
import requests

import os
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")

CHAT_ID = os.getenv("KITCHEN_CHAT_ID")


def send_to_telegram(order, total_price: float):
    text = f"🍽 Новый заказ со стола #{order.table_id}\n"
    text += f"Сумма: {total_price} тг\n"
    text += "Блюда:\n"
    for d in order.order_dishes:
        text += f"— ID {d.dish_id}, x{d.quantity}\n"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

