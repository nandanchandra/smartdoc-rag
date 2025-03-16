from pydantic import BaseModel, Field


class NotifyDocumentUploadRequest(BaseModel):
    original_file: str = Field(..., description="Original file bucket key")
    processed_file: str = Field(..., description="Processed file bucket key")
    bucket: str = Field(..., description="Output bucket")