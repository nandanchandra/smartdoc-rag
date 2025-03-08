from typing import List
from pydantic import BaseModel, Field


class PresignedURLRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    file_name: str = Field(..., description="Name of the file to upload")


class PresignedURLResponse(BaseModel):
    presigned_url: str = Field(
        ..., description="Generated presigned URL for file upload"
    )


class StartMultipartUploadRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    file_name: str = Field(..., description="Name of the file to upload")


class StartMultipartUploadResponse(BaseModel):
    upload_id: str = Field(..., description="Unique upload ID for multipart upload")


class GenerateMultipartPresignedURLRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    file_name: str = Field(..., description="Name of the file to upload")
    upload_id: str = Field(..., description="Unique upload ID for multipart upload")
    part_numbers: int = Field(
        ..., description="Number of parts in the multipart upload"
    )


class GenerateMultipartPresignedURLResponse(BaseModel):
    presigned_urls: List[str] = Field(
        ..., description="List of generated presigned URLs for each upload part"
    )


class CompleteMultipartUploadRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    file_name: str = Field(..., description="Name of the file to upload")
    upload_id: str = Field(..., description="Unique upload ID for multipart upload")
    parts: List[dict] = Field(
        ..., description="List of uploaded parts with part numbers and ETags"
    )


class CompleteMultipartUploadResponse(BaseModel):
    message: str = Field(..., description="Status message for completed upload")
    location: str = Field(..., description="S3 file location")
