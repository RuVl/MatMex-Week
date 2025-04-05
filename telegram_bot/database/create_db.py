import asyncio
from models import Base
from main import engine

async def init_db():
    async with engine.begin() as conn:
        # Удаляем все таблицы (для теста, можно убрать в продакшене)
        await conn.run_sync(Base.metadata.drop_all)
        # Создаём все таблицы
        await conn.run_sync(Base.metadata.create_all)
    print("База данных успешно создана!")

if __name__ == "__main__":
    asyncio.run(init_db())