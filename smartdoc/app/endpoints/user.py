from app.db.database import db_instance
from app.model.user import User
from app.schema.user import CreateUserModel, CreateUserResponseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users")


@router.post("/register")
async def register_user(
    payload: CreateUserModel,
    session: AsyncSession = Depends(db_instance.get_session),
    response_model=CreateUserResponseModel,
):
    await User.exists(session=session, email=payload.email)
    await User.create(session=session, email=payload.email, password=payload.password)
    return {"message": f"{payload.email} registered successfully"}
