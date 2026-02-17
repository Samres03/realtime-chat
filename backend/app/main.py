from fastapi import FastAPI

from app.api.routers import api_router

app = FastAPI(title="Realtime Chat API")
app.include_router(api_router)
