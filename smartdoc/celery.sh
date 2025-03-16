#!/bin/sh

celery -A app.tasks.task.celery_app worker --loglevel=info --concurrency=2 -Q document_ingestions