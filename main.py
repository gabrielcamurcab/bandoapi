from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database import database
from features.auth.routes import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await database.connect()
        yield
    finally:
        await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/api", tags=["users"])