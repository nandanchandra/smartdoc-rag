from app.router import api_router
from app.settings import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

SERVICE_NAME = settings.service_name

app = FastAPI(title=f"{SERVICE_NAME} API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
