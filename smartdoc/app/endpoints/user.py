from app.db.database import db_instance
from app.model.user import User
from app.schema.response import BaseResponseModel
from app.schema.user import CreateUserModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users")


@router.post("/register", response_model=BaseResponseModel)
async def register_user(
    payload: CreateUserModel,
    session: AsyncSession = Depends(db_instance.get_session),
):
    await User.exists(session=session, email=payload.email)
    await User.create(session=session, email=payload.email, password=payload.password)
    return {"message": f"{payload.email} registered successfully"}
