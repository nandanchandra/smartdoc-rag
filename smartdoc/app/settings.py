from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    service_name: str = Field(..., env="SERVICE_NAME")
    allowed_hosts: str = Field(..., env="ALLOWED_HOSTS")

    database_url: str = Field(..., env="DATABASE_URL")

    aws_access_key_id: str = Field(..., env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    aws_s3_region: str = Field(..., env="AWS_S3_REGION")
    aws_s3_bucket_name: str = Field(..., env="AWS_S3_BUCKET_NAME")
    aws_s3_signature_version: str = Field("s3v4", env="AWS_S3_SIGNATURE_VERSION")
    aws_s3_addressing_style: str = Field("virtual", env="AWS_S3_ADDRESSING_STYLE")

    celery_worker_name: str = Field(..., env="CELERY_WORKER_NAME")
    celery_broker_url: str = Field(..., env="CELERY_BROKER_URL")
    celery_backend: str = Field(..., env="CELERY_BACKEND")
    celery_timezone: str = Field("UTC", env="CELERY_TIMEZONE")

    class Config:
        env_file = ".env"


settings = Settings()
