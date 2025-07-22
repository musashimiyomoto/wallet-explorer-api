from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import db_settings

async_engine = create_async_engine(
    url=db_settings.url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_timeout=30,
    pool_recycle=1800,
)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
