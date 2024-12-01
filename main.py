from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database import database
from features.user.routes import router as user_router
from features.posts.routes import router as post_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await database.connect()
        yield
    finally:
        await database.disconnect()

app = FastAPI(lifespan=lifespan,
              title="BandoAPI",
              description="API para praticar Python + FastAPI, com funcionalidades do X/Twitter.",
              version="1.0.0")

app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(post_router, prefix="/api", tags=["posts"])
