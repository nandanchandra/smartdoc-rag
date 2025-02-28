from argon2 import PasswordHasher
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Field, SQLModel, select

ph = PasswordHasher()


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    password: str = Field()

    @classmethod
    async def create(cls, session: AsyncSession, email: str, password: str):
        new_user = cls(email=email, password=ph.hash(password))
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @classmethod
    async def exists(cls, session: AsyncSession, email: str) -> bool:
        result = await session.execute(select(cls).where(cls.email == email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail=f"{email} already exists")
        return False

    async def verify_password(self, plain_password: str) -> bool:
        try:
            return ph.verify(self.password, plain_password)
        except:
            raise ValueError("Invalid password")
