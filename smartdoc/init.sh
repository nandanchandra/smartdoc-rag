#!/bin/sh

uvicorn --reload app.main:app --host=0.0.0.0 --port=${PORT-8000} &

celery -A app.tasks.task.celery_app worker --loglevel=info --concurrency=2 -Q document_ingestions

wait