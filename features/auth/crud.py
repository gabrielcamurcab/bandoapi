from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import User
from .security import hash_password

async def register(db: AsyncSession, username: str, email: str, password: str):
    hashed_password = hash_password(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_email(db: AsyncSession, email: str):
    async with db as session:
        result = await session.execute(select(User).filter(User.email == email))
        return result.scalars().first()