from contextlib import asynccontextmanager

from app.db.database import db_instance
from app.exceptions.base import http_422_error_handler, http_exception_handler
from app.router import api_router
from app.settings import settings
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

SERVICE_NAME = settings.service_name


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_instance.init_db()
    yield
    await db_instance.close_connection()


app = FastAPI(title=f"{SERVICE_NAME} API", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, http_422_error_handler)
