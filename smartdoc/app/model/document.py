from datetime import datetime
from typing import List

from pgvector.sqlalchemy import Vector
from sqlalchemy import Index
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Column, Field, SQLModel


class Document(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id", index=True)
    file_name: str = Field()
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    __table_args__ = (Index("idx_user_id", "user_id"),)

    @classmethod
    async def create(cls, session: AsyncSession, user_id: int, file_name: str):
        new_document = cls(user_id=user_id, file_name=file_name)
        session.add(new_document)
        await session.commit()
        await session.refresh(new_document)
        return new_document


# TODO: index needed?
class DocumentEmbedding(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    document_id: int = Field(foreign_key="document.id")
    user_id: int = Field(foreign_key="user.id")
    embedding: List[float] = Field(
        sa_column=Column(Vector(4096))
    )  # Embedding size of Mistral 7b
    created_at: datetime = Field(default_factory=datetime.utcnow)
