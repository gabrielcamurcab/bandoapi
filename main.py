from fastapi import FastAPI
from database import database, SessionLocal

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

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