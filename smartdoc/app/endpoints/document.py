from app.model.document import Document
from app.schema.document import NotifyDocumentUploadRequest
from app.schema.response import BaseResponseModel
from app.tasks.task import process_uploaded_document
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import db_instance


router = APIRouter(prefix="/document")


@router.post("/notify", response_model=BaseResponseModel)
async def notify_document_upload(
    payload: NotifyDocumentUploadRequest,
    session: AsyncSession = Depends(db_instance.get_session),
):
    await Document.create(
        session=session, user_id=payload.user_id, file_name=payload.file_name
    )
    process_uploaded_document.delay(payload.user_id, payload.file_name)
    return {
        "message": f"{payload.file_name} created successfully for user {payload.user_id}"
    }
