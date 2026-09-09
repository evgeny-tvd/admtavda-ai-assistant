import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from maxapi import Bot, Dispatcher, F
from maxapi.types import MessageCreated
from gigachat import GigaChat
from gigachat.models import ChatCompletionRequest, ChatMessage
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise SystemExit("Ошибка: BOT_TOKEN не найден в .env")

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
giga = GigaChat(model="GigaChat-2", max_retries=2, retry_backoff_factor=1.0)
SYSTEM_PROMPT = (
    "Ты — ИИ-ассистент администрации Тавдинского муниципального округа. "
    "Отвечай вежливо, кратко и по-русски. Если не знаешь ответа — честно скажи об этом."
)


def ask_gigachat(question: str) -> str:
    chat = ChatCompletionRequest(
        messages=[
            ChatMessage(role="system", content=SYSTEM_PROMPT),
            ChatMessage(role="user", content=question)
        ]
    )
    try:
        response = giga.chat.create(chat)
        return response.messages[0].content[0].text
    except Exception as e:
        print(f"GigaChat error: {e}", file=sys.stderr)
        return "Сервис временно недоступен. Попробуйте позже."


@dp.message_created(F.message.body.text)
async def handle_message(event: MessageCreated):
    body = event.message.body
    if body is None or body.text is None:
        return
    text = body.text.strip()
    if not text.startswith("/ask"):
        await event.message.answer(f"Эхо: {text}")
        return
    question = text[len("/ask"):].strip()
    if not question:
        await event.message.answer("Напиши вопрос после /ask, например: /ask Какой график работы администрации?")
        return
    await event.message.answer(ask_gigachat(question))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
