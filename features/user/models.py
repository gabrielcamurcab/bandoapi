from __future__ import annotations
from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy.orm import relationship, Mapped
from core.base import Base

# Inicialize PostDB como None
PostDB = None

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, Sequence('user_id_sequence'), primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    def get_posts(self):
        # Importação tardia de PostDB
        global PostDB
        if PostDB is None:
            from features.posts.models import PostDB
        
        # Buscar posts do usuário
        return PostDB.query.filter_by(user_id=self.id).all()

    # Referência por string usando uma propriedade com importação tardia
    @property
    def posts(self):
        global PostDB
        if PostDB is None:
            from features.posts.models import PostDB
        return PostDB.query.filter_by(user_id=self.id).all()