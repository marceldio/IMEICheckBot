import asyncio
import json
import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from app.config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(
    token=config.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()

# Белый список пользователей (читаем из .env)
WHITE_LIST = set(map(str, os.getenv("WHITE_LIST", "").split(",")))


# Проверка доступа к боту
async def is_allowed_user(user_id: int) -> bool:
    return str(user_id) in WHITE_LIST


# Функция для запроса данных по IMEI
async def check_imei_service(imei: str):
    url = "https://api.imeicheck.net/v1/checks"
    headers = {
        "Authorization": f"Bearer {config.API_TOKEN}",
        "Content-Type": "application/json",
    }
    data = json.dumps({"deviceId": imei, "serviceId": 12})

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {
                    "error": (
                        f"Ошибка {response.status}: "
                        f"{await response.text()}"
                    )
                }


# Хэндлер для команд
@dp.message(Command("start"))
async def send_user_id(message: Message):
    """Отправляет user_id, если пользователь не в белом списке"""
    if not await is_allowed_user(message.from_user.id):
        await message.reply(
            f"Ваш user_id: {message.from_user.id}\n"
            "Отправьте администратору для добавления в белый список."
        )
        return
    await message.reply("Добро пожаловать! Введите IMEI для проверки.")


# Хэндлер для проверки IMEI
@dp.message()
async def handle_imei(message: Message):
    """Проверяет IMEI и отправляет запрос к API"""
    if not await is_allowed_user(message.from_user.id):
        await message.reply("У вас нет доступа к этому боту.")
        return

    imei = message.text.strip()
    if len(imei) != 15 or not imei.isdigit():
        await message.reply("Введите корректный IMEI (15 цифр).")
        return

    await message.reply("Запрашиваю данные, пожалуйста подождите...")

    response = await check_imei_service(imei)

    if "error" in response:
        await message.reply(f"Ошибка при запросе: {response['error']}")
    else:
        imei_info = json.dumps(response, indent=2, ensure_ascii=False)
        await message.reply(
            f"Результат IMEI {imei}:\n<pre>{imei_info}</pre>",
            parse_mode="HTML"
        )


# Запуск бота
async def main():
    logging.info("Запуск Telegram-бота...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
