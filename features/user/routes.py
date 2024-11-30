from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.database import get_db
from .security import login_user, verify_access_token
from .crud import register, get_user_by_email

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class UserCreateResponse(BaseModel):
    message: str
    user_id: int

class Token(BaseModel):
    access_token: str
    refresh_token: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str

@router.post("/user/", response_model=UserCreateResponse)
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


@router.get("/user/", response_model=User)
async def get_user(payload: dict = Depends(verify_access_token), db: Session = Depends(get_db)):
    email = payload.get("sub")  # Assumindo que o e-mail esteja no campo 'sub' do payload
    if not email:
        raise HTTPException(status_code=400, detail="Email not found in token")

    user = await get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user