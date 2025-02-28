from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    service_name: str = Field(..., env="SERVICE_NAME")
    allowed_hosts: str = Field(..., env="ALLOWED_HOSTS")

    database_url: str = Field(..., env="DATABASE_URL")

    class Config:
        env_file = ".env"


settings = Settings()
