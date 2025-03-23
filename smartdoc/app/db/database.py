from app.settings import settings
from app.utils.switch_db_url import get_db_url
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker


class Database:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._async_engine = None
            cls._instance._sync_engine = None
            cls._instance._async_session_factory = None
            cls._instance._sync_session_factory = None
        return cls._instance

    async def init_db(self):
        try:
            self._async_engine = create_async_engine(
                settings.database_url,
                pool_size=100,
                max_overflow=50,
                pool_timeout=30,
                pool_recycle=1800,
            )
            self._async_session_factory = async_sessionmaker(
                bind=self._async_engine, class_=AsyncSession, expire_on_commit=False
            )

            self._sync_engine = create_engine(
                get_db_url(async_mode=False)
            )
            self._sync_session_factory = sessionmaker(bind=self._sync_engine)

            logger.success("Database connection initialized.")
        except Exception as e:
            logger.error(f"Error initializing database connection: {e}")

    async def close_connection(self):
        if self._async_engine:
            await self._async_engine.dispose()
        if self._sync_engine:
            self._sync_engine.dispose()

    async def get_async_session(self):
        async with self._async_session_factory() as session:
            yield session

    def get_sync_session(self):
        return self._sync_session_factory()


db_instance = Database()
