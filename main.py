from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database, SessionLocal

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/db")
async def db():
    query = "SELECT * FROM users"
    result = await database.fetch_all(query)
    return {"data": result}