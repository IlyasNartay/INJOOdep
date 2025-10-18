from telegram_bot.bot_instance import dp, bot
from app.database import SessionLocal
from app.models import Order, TelegramUser, Address
from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardButton as AioInlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup as AioInlineKeyboardMarkup

REGISTER_CODES = {
    "kitchen123": "kitchen",
    "courier456": "courier"
}


async def send_order_to_kitchen(order_data: dict):
    db = SessionLocal()
    try:
        # 1. Получаем адрес
        address = db.query(Address).filter(Address.id == order_data['address_id']).first()
        if not address:
            address_text = "Адрес не найден"
        else:
            try:
                address_text = address.full_address()
            except Exception as e:
                print(f"⚠️ Ошибка при вызове address.full_address(): {e}")
                address_text = "Ошибка адреса"

        # 2. Формируем список блюд
        dish_lines = []
        for dish in order_data.get("dishes", []):
            try:
                name = dish.get("name") if isinstance(dish, dict) else getattr(dish, "name", "неизвестно")
                quantity = dish.get("quantity") if isinstance(dish, dict) else getattr(dish, "quantity", "неизвестно")
                dish_lines.append(f"{name} × {quantity}")
            except Exception as e:
                print(f"⚠️ Ошибка при разборе блюда: {dish} — {e}")
                continue

        message = (
                f"🧾 <b>Новый заказ #{order_data['id']}</b>\n\n"
                f"👤 <b>Пользователь ID:</b> <code>{order_data['user_id']}</code>\n"
                f"📍 <b>Адрес:</b> {address_text}\n"
                f"💰 <b>Сумма:</b> {order_data['total_price']} ₸\n"
                f"📦 <b>Статус:</b> <i>{order_data['status']}</i>\n\n"
                f"🍽 <b>Блюда:</b>\n"
                f"```\n" +
                "\n".join([f"{line}" for line in dish_lines]) +
                "\n```"
        )

        # 4. Inline-кнопка
        markup = AioInlineKeyboardMarkup(
            inline_keyboard=[
                [AioInlineKeyboardButton(text="✅ Готово", callback_data=f"ready:{order_data['id']}")]
            ]
        )

        # 5. Отправка всем кухням
        kitchens = db.query(TelegramUser).filter(TelegramUser.role == "kitchen").all()
        print(f"🔔 Кухонь найдено: {len(kitchens)}")

        for kitchen in kitchens:
            if not kitchen.chat_id:
                print(f"⚠️ У пользователя с id={kitchen.id} отсутствует chat_id")
                continue
            try:
                print(f"📤 Отправка сообщения кухне chat_id={kitchen.chat_id}")
                await bot.send_message(
                    chat_id=int(kitchen.chat_id),
                    text=message,
                    reply_markup=markup,
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"❌ Ошибка отправки сообщения кухне {kitchen.chat_id}: {e}")

    except Exception as global_error:
        print(f"💥 Ошибка в send_order_to_kitchen: {global_error}")
    finally:
        db.close()

# Регистрация по коду
@dp.message()
async def handle_registration(message: Message):
    code = message.text.strip()
    chat_id = str(message.chat.id)

    if code not in REGISTER_CODES:
        await message.reply("❌ Неверный код регистрации.")
        return

    role = REGISTER_CODES[code]
    db = SessionLocal()
    try:
        user = db.query(TelegramUser).filter(TelegramUser.chat_id == chat_id).first()
        if not user:
            user = TelegramUser(chat_id=chat_id, role=role)
            db.add(user)
            db.commit()
            await message.reply(f"✅ Регистрация успешна! Ваша роль: {role}")
        else:
            await message.reply(f"🔒 Вы уже зарегистрированы как {user.role}")
    finally:
        db.close()

# Кнопка "Готово" от кухни
@dp.callback_query(lambda c: c.data.startswith("ready:"))
async def order_ready(callback: CallbackQuery):
    chat_id = str(callback.from_user.id)
    order_id = int(callback.data.split(":")[1])

    db = SessionLocal()
    try:
        user = db.query(TelegramUser).filter(TelegramUser.chat_id == chat_id).first()
        if not user or user.role != "kitchen":
            await callback.answer("❌ Только кухня может это делать.", show_alert=True)
            return

        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            await callback.answer("❌ Заказ не найден.", show_alert=True)
            return

        order.status = "ready"
        db.commit()

        # Удалить кнопку после нажатия
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except Exception as e:
            print(f"❌ Не удалось удалить кнопку 'Готово': {e}")

        await callback.answer("✅ Отправлено курьерам.")

        # Получаем адрес
        address = db.query(Address).filter(Address.id == order.address_id).first()
        address_text = address.full_address() if address else "Адрес не найден"

        couriers = db.query(TelegramUser).filter(TelegramUser.role == "courier").all()
        markup = AioInlineKeyboardMarkup(
            inline_keyboard=[
                [AioInlineKeyboardButton(text="Доставлено", callback_data=f"delivered:{order.id}")]
            ]
        )
        for courier in couriers:
            try:
                await bot.send_message(
                    chat_id=int(courier.chat_id),
                    text=(
                        f"🚚 Заказ #{order.id} готов к доставке!\n"
                        f"📍 Адрес: {address_text}"
                    ),
                    reply_markup=markup
                )
            except Exception as e:
                print(f"❌ Ошибка при отправке курьеру {courier.chat_id}: {e}")

        await callback.answer("✅ Отправлено курьерам.")
    finally:
        db.close()

@dp.callback_query(lambda c: c.data.startswith("delivered:"))
async def order_done(callback: CallbackQuery):
    chat_id = str(callback.from_user.id)
    order_id = int(callback.data.split(":")[1])

    db = SessionLocal()
    try:
        user = db.query(TelegramUser).filter(TelegramUser.chat_id == chat_id).first()
        if not user or user.role != "courier":
            await callback.answer("❌ Только курьер может завершить заказ.", show_alert=True)
            return

        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            await callback.answer("❌ Заказ не найден.", show_alert=True)
            return

        order.status = "done"
        db.commit()

        await callback.message.edit_text(f"✅ Заказ #{order.id} доставлен!")
        await callback.answer("Спасибо!")
    finally:
        db.close()