from app.endpoints.user import router as user_router
from app.endpoints.s3 import router as s3_router
from app.endpoints.document import router as document_router
from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user_router)
api_router.include_router(s3_router)
api_router.include_router(document_router)


@api_router.get("/")
def test():
    return "Hello World"
