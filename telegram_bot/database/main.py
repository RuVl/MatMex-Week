from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from database.env import PostgresKeys

engine = create_async_engine(PostgresKeys.URL)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)
