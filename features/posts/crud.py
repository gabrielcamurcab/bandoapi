from sqlalchemy.ext.asyncio import AsyncSession
from .models import PostCreate, PostDB
from ..user.models import User
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