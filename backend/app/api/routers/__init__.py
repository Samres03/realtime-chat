from fastapi import APIRouter

from app.api.routers import status

api_router = APIRouter()
api_router.include_router(status.router, tags=["status"])
