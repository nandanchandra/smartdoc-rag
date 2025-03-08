from sqlmodel import SQLModel, Field
from datetime import datetime

class Document(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    file_name: str = Field()
    s3_key: str = Field()
    uploaded_at: datetime = Field()
