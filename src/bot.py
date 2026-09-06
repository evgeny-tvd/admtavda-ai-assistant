import asyncio
import logging
import os

from dotenv import load_dotenv
from maxapi import Bot, Dispatcher, F
from maxapi.types import MessageCreated

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise SystemExit("Ошибка: BOT_TOKEN не найден в .env")

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message_created(F.message.body.text)
async def echo(event: MessageCreated):
    body = event.message.body
    if body is None or body.text is None:
        return
    await event.message.answer(f"Эхо: {body.text}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    