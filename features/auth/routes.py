from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.database import get_db
from .security import login_user
from .crud import register, get_user_by_email

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

@router.post("/users/")
async def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = await register(db, user.username, user.email, user.password)
        return {"message": "Usuário criado com sucesso!", "user_id": new_user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login/", response_model=Token)
async def login_route(login_request: LoginRequest, db: Session = Depends(get_db)):
    email = login_request.email
    password = login_request.password
    return await login_user(db, email, password)