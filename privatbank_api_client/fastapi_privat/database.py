import os
from dotenv import load_dotenv
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


load_dotenv()

DB_URI = os.getenv("DB_URI", "postgres:postgres@localhost:5432/postgres")

ASYNC_DATABASE_URI = f"postgresql+asyncpg://{DB_URI}"

engine = create_async_engine(ASYNC_DATABASE_URI, poolclass=NullPool)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
