from app.celery import celery_app
from app.services.s3_client import s3_client
from app.utils.file_utils import decode_s3_content
from loguru import logger

logger.add("logs/celery_worker.log", rotation="10MB", retention="10 days", level="INFO")


@celery_app.task()
def process_uploaded_document(key: str, bucket: str):

    s3_response = s3_client.get_object(bucket, key)
    extracted_text = decode_s3_content(s3_response)

    logger.info(f"Retrieved document content of size: {len(extracted_text)}: {extracted_text}")

    if extracted_text:
        logger.info(f"Text successfully extracted from document {key}")
    else:
        logger.info(f"No text extracted from document {key} ,{extracted_text}")
