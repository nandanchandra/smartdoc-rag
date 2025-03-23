from app.celery import celery_app
from app.db.database import db_instance
from app.llm.pgvector_client import pgvector_client
from app.model.document import Document
from app.services.s3_client import s3_client
from app.utils.file_utils import decode_s3_content
from app.utils.s3_user_map import extract_user_id_filename
from loguru import logger

logger.add("logs/celery_worker.log", rotation="10MB", retention="10 days", level="INFO")


def fetch_document_text(bucket: str, key: str) -> str:
    s3_response = s3_client.get_object(bucket, key)
    extracted_text = decode_s3_content(s3_response)
    return extracted_text


def store_document(user_id: str, file_name: str, text: str) -> Document:
    session = db_instance.get_sync_session()
    try:
        collection = pgvector_client.generate_document_embeddings(
            user_id, text, file_name
        )
        document = Document.create(
            session, user_id=user_id, file_name=file_name, collection=collection
        )
        return document
    except Exception as e:
        session.rollback()
        logger.error(
            f"Database transaction failed for user {user_id}, file {file_name}: {str(e)}"
        )
        raise
    finally:
        session.close()


@celery_app.task()
def process_uploaded_document(old_key, new_key: str, bucket: str):

    text_to_process = fetch_document_text(bucket, new_key)

    user_id, file_name = extract_user_id_filename(old_key)

    document = store_document(user_id, file_name, text_to_process)

    logger.info(
        f"Successfully processed and stored document: {new_key} (ID: {document.id})"
    )
