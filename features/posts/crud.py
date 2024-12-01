from sqlalchemy.ext.asyncio import AsyncSession
from .models import PostCreate, PostDB
from ..user.models import User
from sqlalchemy.future import select
from ..user.crud import get_user_by_email
from fastapi import HTTPException

async def create_post(db: AsyncSession, user_email: str, post_data: PostCreate):
    async with db as session:
        user = await get_user_by_email(db, user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        new_post = PostDB(
            content=post_data.content,
            reply_for=post_data.reply_for,
            user_id=user.id
        )

        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)
        return new_post
    
async def get_posts_by_user(db: AsyncSession, user_id: int):
    async with db as session:
        result = await session.execute(select(PostDB).filter(PostDB.user_id == user_id, PostDB.is_deleted == False))
        posts = result.scalars().all()
        return posts
    
async def delete_post(db: AsyncSession, post_id: int, user_email = str):
    async with db as session:
        user = await get_user_by_email(db, user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        result = await session.execute(select(PostDB).filter(PostDB.id == post_id, PostDB.user_id == user.id, PostDB.is_deleted == False))
        post = result.scalars().first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        post.is_deleted = True
        await session.commit()
        return post