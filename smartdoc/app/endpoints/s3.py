from app.schema.s3 import (
    CompleteMultipartUploadRequest,
    CompleteMultipartUploadResponse,
    GenerateMultipartPresignedURLRequest,
    GenerateMultipartPresignedURLResponse,
    PresignedURLRequest,
    PresignedURLResponse,
    StartMultipartUploadRequest,
    StartMultipartUploadResponse,
)
from app.services.s3_client import s3_client
from fastapi import APIRouter


router = APIRouter(prefix="/s3")


@router.post("/generate_presigned_url", response_model=PresignedURLResponse)
def generate_presigned_url(payload: PresignedURLRequest):
    url = s3_client.generate_presigned_url(payload.user_id, payload.file_name)
    return PresignedURLResponse(presigned_url=url)


@router.post("/start_multipart_upload", response_model=StartMultipartUploadResponse)
def start_multipart_upload(request: StartMultipartUploadRequest):
    upload_id = s3_client.start_multipart_upload(request.user_id, request.file_name)
    return StartMultipartUploadResponse(upload_id=upload_id)


@router.post(
    "/generate_multipart_presigned_urls",
    response_model=GenerateMultipartPresignedURLResponse,
)
def generate_multipart_presigned_urls(request: GenerateMultipartPresignedURLRequest):
    urls = s3_client.generate_multipart_presigned_urls(
        request.user_id, request.file_name, request.upload_id, request.part_numbers
    )
    return GenerateMultipartPresignedURLResponse(presigned_urls=urls)


@router.post(
    "/complete_multipart_upload", response_model=CompleteMultipartUploadResponse
)
def complete_multipart_upload(request: CompleteMultipartUploadRequest):
    response = s3_client.complete_multipart_upload(
        request.user_id, request.file_name, request.upload_id, request.parts
    )
    return CompleteMultipartUploadResponse(
        message="Multipart upload completed successfully",
        location=response["Location"],
    )
