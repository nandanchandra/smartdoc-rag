from datetime import datetime
from typing import Optional

from sqlalchemy import Index
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel


class Document(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id", index=True)
    file_name: str = Field()
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    collection: Optional[str] = Field(default=None, index=True)

    __table_args__ = (Index("idx_user_id", "user_id"),)

    @classmethod
    def create(cls, session: Session, user_id: int, file_name: str, collection: str):
        new_document = cls(user_id=user_id, file_name=file_name, collection=collection)
        session.add(new_document)
        session.commit()
        session.refresh(new_document)
        return new_document