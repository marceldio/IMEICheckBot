from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import config

# Создаем асинхронный движок для PostgreSQL
engine = create_async_engine(config.DATABASE_URL, future=True, echo=True)

# Создаем фабрику сессий
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Функция для получения сессии
async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
