from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

sync_engine = create_engine(DATABASE_URL, echo=True)

async_engine = create_async_engine(DATABASE_URL, echo=True)

SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)
