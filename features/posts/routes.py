from fastapi import APIRouter, Depends, HTTPException, status
from ..user.security import verify_access_token
from .crud import create_post, get_posts_by_user
from .models import PostCreate, PostCreateResponse, PostResponse
from core.database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("/post", response_model=PostCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_new_post(post_data: PostCreate, payload: dict = Depends(verify_access_token), db: Session = Depends(get_db)):
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=400, detail="Email not found in token")
    
    new_post = await create_post(db, email, post_data)
    return {"message": "Post publicado com sucesso!", "id": new_post.id}

@router.get("/posts/{user_id}", response_model=List[PostResponse], status_code=status.HTTP_200_OK)
async def get_posts_by_user_route(user_id: int, db: Session = Depends(get_db)):
    posts = await get_posts_by_user(db, user_id)
    return posts