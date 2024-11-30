from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from datetime import datetime, timedelta, timezone
from typing import Union
from passlib.context import CryptContext
from .models import User
from fastapi import Request, HTTPException, Depends
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Função de login
async def login_user(db: Session, email: str, password: str):
    # Buscar o usuário pelo email
    async with db as session:
        result = await session.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verificar se a senha está correta
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Gerar o token JWT
    access_token_expires = timedelta(minutes=30)
    refresh_token_expires = timedelta(days=7)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    refresh_token = create_access_token(data={"sub": user.email}, expires_delta=refresh_token_expires)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta + expires_delta
    else:
        expire = datetime.now(timezone.utc) + expires_delta + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(request: Request):
    # Extrai o token do cabeçalho Authorization
    token = request.headers.get("Authorization")
    
    if token is None:
        raise HTTPException(status_code=401, detail="Authorization token is missing")
    
    try:
        # Remove o prefixo "Bearer" se houver
        token = token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])  # Verifica a assinatura e decodifica o token
        return payload  # Retorna o payload do token para ser usado na rota
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")