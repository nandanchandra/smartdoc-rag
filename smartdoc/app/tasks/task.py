from app.services import s3_client
from app.celery import celery_app
from io import BytesIO
from PyPDF2 import PdfReader
from starlette.datastructures import UploadFile
from loguru import logger


def extract_text_from_document(input_data):

    text = ""
    if isinstance(input_data, BytesIO):
        pdf_reader = PdfReader(input_data)
        text = "".join(
            page.extract_text() for page in pdf_reader.pages if page.extract_text()
        )

    elif isinstance(input_data, UploadFile):
        pdf_reader = PdfReader(BytesIO(input_data.read()))
        text = "".join(
            page.extract_text() for page in pdf_reader.pages if page.extract_text()
        )

    elif isinstance(input_data, str):
        text = input_data

    return text


@celery_app.task
def process_uploaded_document(user_id: str, file_name: str):

    key = f"{user_id}/{file_name}"

    s3_response = s3_client.s3_client.get_object(
        Bucket=s3_client.bucket_name, Key=key
    )

    extracted_text = extract_text_from_document(s3_response["Body"].read())