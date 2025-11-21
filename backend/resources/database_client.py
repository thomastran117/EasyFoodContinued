from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config.environmentConfig import settings
from utilities.logger import logger

DATABASE_URL = settings.database_url
MODE = settings.mode

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def init_database():
    try:
        if MODE in {"ci", "testing", "test"}:
            logger.info("Skipping database connection")

        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise


@asynccontextmanager
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
