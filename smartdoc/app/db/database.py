from app.settings import settings
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)


class Database:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._engine = None
            cls._instance._async_session_factory = None
        return cls._instance

    async def init_db(self):
        self._engine = create_async_engine(
            settings.database_url,
            pool_size=100,
            max_overflow=50,
            pool_timeout=30,
            pool_recycle=1800,
        )
        self._async_session_factory = async_sessionmaker(
            bind=self._engine, class_=AsyncSession, expire_on_commit=False
        )

    async def close_connection(self):
        if self._engine:
            await self._engine.dispose()

    async def get_session(self):
        async with self._async_session_factory() as session:
            yield session


db_instance = Database()
