from app import settings
from sqlmodel import SQLModel, Field
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

class Document(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    file_name: str = Field()
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    async def create(cls, session: AsyncSession, user_id: int, file_name: str):
        new_document = cls(user_id=user_id, file_name=file_name)
        session.add(new_document)
        await session.commit()
        await session.refresh(new_document)
        return new_document
    
