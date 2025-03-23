from app.schema.document import NotifyDocumentUploadRequest
from app.schema.response import BaseResponseModel
from app.tasks.task import process_uploaded_document
from fastapi import APIRouter

router = APIRouter(prefix="/document")


@router.post("/notify", 
                response_model=BaseResponseModel
            )
def notify_document_upload(
    payload: NotifyDocumentUploadRequest,
):
    process_uploaded_document(payload.original_file, payload.processed_file, payload.bucket)
    return {"message": "ok"}
