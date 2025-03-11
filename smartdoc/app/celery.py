from app.settings import settings
from celery import Celery

celery_app = Celery(
    settings.celery_worker_name,
    broker=settings.celery_broker_url,
    backend=settings.celery_backend,
)

celery_app.conf.timezone = settings.celery_timezone

celery_app.conf.task_routes = {"app.tasks.*": {"queue": "document_ingestions"}}