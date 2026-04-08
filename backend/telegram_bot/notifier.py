from aiogram.types import InlineKeyboardButton as AioInlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup as AioInlineKeyboardMarkup

from app.constants.order_status import ORDER_STATUS_LABELS, OrderStatus
from app.database import SessionLocal
from app.models import Address, TelegramUser
from telegram_bot.bot_instance import bot


async def send_order_to_admin(order_data: dict):
    db = SessionLocal()
    try:
        address = db.query(Address).filter(Address.id == order_data.get("address_id")).first()
        address_text = address.full_address() if address else "Адрес не найден"

        dish_lines = []
        for dish in order_data.get("dishes", []):
            try:
                name = dish.get("name", "неизвестно") if isinstance(dish, dict) else getattr(dish, "name", "неизвестно")
                quantity = dish.get("quantity", "неизвестно") if isinstance(dish, dict) else getattr(dish, "quantity", "неизвестно")
                dish_lines.append(f"  - {name} x {quantity}")
            except Exception as error:
                print(f"Ошибка при разборе блюда {dish}: {error}")

        note_text = order_data.get("note") or "Без комментария"
        message = (
            f"<b>НОВЫЙ ЗАКАЗ #{order_data['id']}</b>\n\n"
            f"<b>Пользователь ID:</b> <code>{order_data['user_id']}</code>\n"
            f"<b>Адрес:</b> {address_text}\n"
            f"<b>Сумма:</b> {order_data['total_price']} тг\n"
            f"<b>Kaspi:</b> {order_data['kaspi_number']}\n"
            f"<b>Комментарий:</b> {note_text}\n"
            f"<b>Статус:</b> <i>{ORDER_STATUS_LABELS[OrderStatus.pending.value]}</i>\n\n"
            f"<b>Блюда:</b>\n"
            f"<pre>{chr(10).join(dish_lines)}</pre>"
        )

        markup = AioInlineKeyboardMarkup(
            inline_keyboard=[
                [
                    AioInlineKeyboardButton(
                        text="Подтвердить и отправить на кухню",
                        callback_data=f"admin_confirm:{order_data['id']}",
                    )
                ]
            ]
        )

        admins = db.query(TelegramUser).filter(TelegramUser.role == "admin").all()
        for admin in admins:
            if not admin.chat_id:
                continue

            try:
                await bot.send_message(
                    chat_id=int(admin.chat_id),
                    text=message,
                    reply_markup=markup,
                    parse_mode="HTML",
                )
            except Exception as error:
                print(f"Ошибка отправки сообщения администратору {admin.chat_id}: {error}")
    except Exception as error:
        print(f"Ошибка в send_order_to_admin: {error}")
    finally:
        db.close()


async def send_table_order_to_kitchen(order_data: dict):
    db = SessionLocal()
    try:
        dish_lines = []
        for dish in order_data.get("dishes", []):
            try:
                name = dish.get("name") if isinstance(dish, dict) else getattr(dish, "name", "неизвестно")
                quantity = dish.get("quantity") if isinstance(dish, dict) else getattr(dish, "quantity", "неизвестно")
                dish_lines.append(f"  - {name} x {quantity}")
            except Exception as error:
                print(f"Ошибка при разборе блюда {dish}: {error}")

        message = (
            f"<b>Новый заказ в зале #{order_data['id']}</b>\n\n"
            f"<b>Стол:</b> {order_data['table_id']}\n"
            f"<b>Сумма:</b> {order_data['total_price']} тг\n"
            f"<b>Блюда:</b>\n"
            f"<pre>{chr(10).join(dish_lines)}</pre>"
        )

        kitchens = db.query(TelegramUser).filter(TelegramUser.role == "kitchen").all()
        for kitchen in kitchens:
            if not kitchen.chat_id:
                continue

            try:
                await bot.send_message(
                    chat_id=int(kitchen.chat_id),
                    text=message,
                    parse_mode="HTML",
                )
            except Exception as error:
                print(f"Ошибка отправки сообщения кухне {kitchen.chat_id}: {error}")
    except Exception as error:
        print(f"Ошибка в send_table_order_to_kitchen: {error}")
    finally:
        db.close()
