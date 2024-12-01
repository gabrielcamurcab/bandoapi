from __future__ import annotations
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Sequence
from sqlalchemy.orm import relationship, Mapped
from core.base import Base
from typing import Optional

# Inicialize User como None
User = None

class PostCreate(BaseModel):
    content: str
    reply_for: Optional[int] = None

    class Config:
        orm_mode = True

class Post(BaseModel):
    id: int
    content: str
    user_id: int

    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    message: str
    id: int

class PostDB(Base):
    __tablename__ = "posts"

    id = Column(Integer, Sequence('posts_id_seq'), primary_key=True, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    reply_for = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE", use_alter=True))
    is_deleted = Column(Boolean, default=False)

    def get_user(self):
        # Importação tardia do usuário
        global User
        if User is None:
            from features.user.models import User
        
        # Buscar o usuário relacionado
        return User.query.get(self.user_id)

    # Referência por string usando uma propriedade com importação tardia
    @property
    def user(self):
        global User
        if User is None:
            from features.user.models import User
        return User.query.get(self.user_id)