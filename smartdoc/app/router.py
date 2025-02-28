from app.endpoints.user import router as user_router
from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user_router)


@api_router.get("/")
def test():
    return "Hello World"
