from fastapi import APIRouter

from app.api.routers import auth, status, chat, message

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(status.router, tags=["status"])
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(message.router, tags=["message"])
