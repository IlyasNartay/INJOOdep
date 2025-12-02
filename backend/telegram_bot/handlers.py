from telegram_bot.bot_instance import dp, bot
from app.database import SessionLocal
# Необходимые модели должны быть импортированы из вашего файла app.models
from app.models import Order, TelegramUser, Address
from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardButton as AioInlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup as AioInlineKeyboardMarkup

# Коды для регистрации пользователей с разными ролями
REGISTER_CODES = {
    "kitchen123": "kitchen",
    "courier456": "courier",
    "admin1789" : "admin",
}

# =========================================================================
# ФУНКЦИЯ: ОТПРАВКА ЗАКАЗА АДМИНИСТРАТОРУ НА ПОДТВЕРЖДЕНИЕ
# =========================================================================
async def send_order_to_admin(order_data: dict):
    """Отправляет новый заказ администраторам для первичного подтверждения."""
    db = SessionLocal()
    try:
        # 1. Получаем адрес
        address = db.query(Address).filter(Address.id == order_data.get('address_id')).first()
        address_text = address.full_address() if address else "Адрес не найден"

        # 2. Формируем список блюд
        dish_lines = []
        for dish in order_data.get("dishes", []):
            try:
                # Предполагаем, что dish - это словарь или объект с атрибутами
                name = dish.get("name", "неизвестно") if isinstance(dish, dict) else getattr(dish, "name", "неизвестно")
                quantity = dish.get("quantity", "неизвестно") if isinstance(dish, dict) else getattr(dish, "quantity", "неизвестно")
                dish_lines.append(f"  — {name} × {quantity}")
            except Exception as e:
                print(f"⚠️ Ошибка при разборе блюда: {dish} — {e}")
                continue

        # 3. Формируем сообщение
        message = (
                f"🚨 <b>НОВЫЙ ЗАКАЗ (Требует подтверждения) #{order_data['id']}</b>\n\n"
                f"👤 <b>Пользователь ID:</b> <code>{order_data['user_id']}</code>\n"
                f"📍 <b>Адрес:</b> {address_text}\n"
                f"💰 <b>Сумма:</b> {order_data['total_price']} ₸\n"
                f"📦 <b>Статус:</b> <i>Ожидает подтверждения</i>\n\n"
                f"🍽 <b>Блюда:</b>\n"
                f"```\n" +
                f"  =====================\n" +  # Верхний разделитель внутри блока
                "\n".join(dish_lines) +
                f"\n  =====================" +  # Нижний разделитель внутри блока
                "\n```"
        )

        # 4. Inline-кнопка для подтверждения
        # ВНИМАНИЕ: Передача всей переменной 'message' в callback_data
        # может вызвать ошибку "Callback data is too long" (лимит 64 байта).
        # ИСПРАВЛЕНО: Передаем только order_id, чтобы избежать ошибки BUTTON_DATA_INVALID.
        markup = AioInlineKeyboardMarkup(
            inline_keyboard=[
                [AioInlineKeyboardButton(text="✅ Подтвердить и отправить на кухню", callback_data=f"admin_confirm:{order_data['id']}")]
            ]
        )

        # 5. Отправка всем администраторам
        admins = db.query(TelegramUser).filter(TelegramUser.role == "admin").all()
        print(f"🔔 Администраторов найдено: {len(admins)}")

        for admin in admins:
            if not admin.chat_id:
                print(f"⚠️ У администратора с id={admin.id} отсутствует chat_id")
                continue
            try:
                print(f"📤 Отправка сообщения администратору chat_id={admin.chat_id}")
                await bot.send_message(
                    chat_id=int(admin.chat_id),
                    text=message,
                    reply_markup=markup,
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"❌ Ошибка отправки сообщения администратору {admin.chat_id}: {e}")

    except Exception as global_error:
        print(f"💥 Ошибка в send_order_to_admin: {global_error}")
    finally:
        db.close()


# =========================================================================
# ФУНКЦИЯ: ОТПРАВКА ЗАКАЗА НА КУХНЮ
# =========================================================================
async def send_order_to_kitchen(order_data: dict):
    """Отправляет подтвержденный заказ на кухню."""
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
                # Добавляем отступ и маркер для каждой строки
                dish_lines.append(f"  — {name} × {quantity}")
            except Exception as e:
                print(f"⚠️ Ошибка при разборе блюда: {dish} — {e}")
                continue

        # 3. Формируем сообщение
        message = (
                f"🧾 <b>Новый заказ #{order_data['id']}</b>\n\n"
                f"👤 <b>Пользователь ID:</b> <code>{order_data['user_id']}</code>\n"
                f"📍 <b>Адрес:</b> {address_text}\n"
                f"💰 <b>Сумма:</b> {order_data['total_price']} ₸\n"
                f"📦 <b>Статус:</b> <i>{order_data['status']}</i>\n\n"
                f"🍽 <b>Блюда:</b>\n"
                f"```\n" +
                f"  =====================\n" +  # Верхний разделитель внутри блока
                "\n".join(dish_lines) +
                f"\n  =====================" +  # Нижний разделитель внутри блока
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

# =========================================================================
# ФУНКЦИЯ: ОТПРАВКА ЗАКАЗА СО СТОЛА НА КУХНЮ (Без адреса)
# =========================================================================
async def send_table_order_to_kitchen(order_data: dict):
    """Отправляет заказ со стола (без доставки) на кухню."""
    db = SessionLocal()
    try:
        dish_lines = []
        for dish in order_data.get("dishes", []):
            try:
                name = dish.get("name") if isinstance(dish, dict) else getattr(dish, "name", "неизвестно")
                quantity = dish.get("quantity") if isinstance(dish, dict) else getattr(dish, "quantity", "неизвестно")
                # Добавляем отступ и маркер для каждой строки
                dish_lines.append(f"  — {name} × {quantity}")
            except Exception as e:
                print(f"⚠️ Ошибка при разборе блюда: {dish} — {e}")
                continue

        # 3. Формируем сообщение
        message = (
                f"🧾 <b>Новый заказ #{order_data['id']}</b>\n\n"
                f"📍 <b> Cтол :</b> {order_data['table_id']}\n"
                f"💰 <b>Сумма:</b> {order_data['total_price']} ₸\n"
                f"🍽 <b>Блюда:</b>\n"
                f"```\n" +
                f"  =====================\n" +  # Верхний разделитель внутри блока
                "\n".join(dish_lines) +
                f"\n  =====================" +  # Нижний разделитель внутри блока
                "\n```"
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
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"❌ Ошибка отправки сообщения кухне {kitchen.chat_id}: {e}")

    except Exception as global_error:
        print(f"💥 Ошибка в send_order_to_kitchen: {global_error}")
    finally:
        db.close()

# =========================================================================
# ОБРАБОТЧИК: ПОДТВЕРЖДЕНИЕ ЗАКАЗА АДМИНИСТРАТОРОМ
# =========================================================================
@dp.callback_query(lambda c: c.data.startswith("admin_confirm:"))
async def confirm_order(callback: CallbackQuery):
    """Обрабатывает нажатие кнопки подтверждения заказа администратором.
    После подтверждения отправляет заказ на кухню."""
    chat_id = str(callback.from_user.id)
    # Извлекаем ID из callback_data (формат: admin_confirm:ID)
    try:
        # Теперь data.split(":") вернет ['admin_confirm', 'ID']
        order_id = int(callback.data.split(":")[1])
    except Exception:
        # Fallback, если формат ID нарушен
        await callback.answer("❌ Неверный формат ID заказа.", show_alert=True)
        return

    db = SessionLocal()
    try:
        user = db.query(TelegramUser).filter(TelegramUser.chat_id == chat_id).first()
        if not user or user.role != "admin":
            await callback.answer("❌ Только администратор может это делать.", show_alert=True)
            return

        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            await callback.answer("❌ Заказ не найден.", show_alert=True)
            return

        # 1. Обновляем статус заказа в базе данных
        order.status = "accepted"
        db.commit()

        # 2. Формируем словарь order_data для отправки на кухню
        order_dict = {
            'id': order.id,
            'user_id': order.user_id,
            'address_id': order.address_id,
            'total_price': order.total_price,
            'status': order.status, # 'confirmed'
            "dishes": [
                {
                    "name": d.name,
                    "price": d.price,
                    "quantity": next(item.quantity for item in order.dishes if item.dish_id == d.id)
                }
                for d in order.order_dishes
            ],
        }

        # 3. Отправляем заказ на кухню
        await send_order_to_kitchen(order_dict)

        # 4. Редактируем сообщение администратора
        await callback.message.edit_text(
            f"✅ <b>Заказ #{order_id} ПОДТВЕРЖДЕН.</b>\n\n"
            f"Сообщение успешно отправлено на кухню.",
            reply_markup=None,
            parse_mode="HTML"
        )
        await callback.answer("✅ Заказ подтвержден и отправлен на кухню.")

    except Exception as global_error:
        print(f"💥 Ошибка в confirm_order: {global_error}")
        await callback.answer("❌ Произошла ошибка при подтверждении заказа.")
    finally:
        db.close()


# =========================================================================
# ОБРАБОТЧИК: РЕГИСТРАЦИЯ ПО КОДУ
# =========================================================================
@dp.message()
async def handle_registration(message: Message):
    """Обрабатывает ввод кода для назначения роли."""
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

# =========================================================================
# ОБРАБОТЧИК: КНОПКА "ГОТОВО" ОТ КУХНИ
# =========================================================================
@dp.callback_query(lambda c: c.data.startswith("ready:"))
async def order_ready(callback: CallbackQuery):
    """Обрабатывает нажатие кнопки "Готово" от пользователя с ролью кухни."""
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

        # Удалить кнопку "Готово" после нажатия
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except Exception as e:
            print(f"❌ Не удалось удалить кнопку 'Готово': {e}")

        await callback.answer("✅ Отправлено курьерам.")

        # Получаем адрес
        address = db.query(Address).filter(Address.id == order.address_id).first()
        address_text = address.full_address() if address else "Адрес не найден"

        # Уведомляем курьеров
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

    finally:
        db.close()

# =========================================================================
# ОБРАБОТЧИК: КНОПКА "ДОСТАВЛЕНО" ОТ КУРЬЕРА
# =========================================================================
@dp.callback_query(lambda c: c.data.startswith("delivered:"))
async def order_done(callback: CallbackQuery):
    """Обрабатывает нажатие кнопки "Доставлено" от пользователя с ролью курьера."""
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

        # Редактируем сообщение курьера
        await callback.message.edit_text(f"✅ Заказ #{order.id} доставлен!")
        await callback.answer("Спасибо!")
    finally:
        db.close()