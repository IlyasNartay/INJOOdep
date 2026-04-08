import asyncio

from telegram_bot.bot_instance import bot, dp
from telegram_bot import handlers  # noqa: F401


async def run_polling() -> None:
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def main() -> None:
    asyncio.run(run_polling())


if __name__ == "__main__":
    main()
