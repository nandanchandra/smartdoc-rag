from app.settings import settings

def get_db_url(async_mode: bool = True) -> str:
    database_url = settings.database_url
    return database_url if async_mode else database_url.replace("postgresql+asyncpg", "postgresql")