from pydantic import BaseModel, Field


class NotifyDocumentUploadRequest(BaseModel):
    user_id: int = Field(..., description="Unique identifier for the user")
    file_name: str = Field(..., description="Name of the file uploaded")