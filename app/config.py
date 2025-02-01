import os

from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()


class Config:
    # База данных
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")

    DATABASE_URL = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # API токен IMEICheck
    API_TOKEN = os.getenv("API_TOKEN")

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # JWT токены
    SECRET_KEY = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    # Белый список пользователей
    WHITE_LIST = os.getenv("WHITE_LIST", "").split(",")


config = Config()
