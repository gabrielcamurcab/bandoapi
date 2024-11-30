from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
import os
from dotenv import load_dotenv

# Carregando variáveis de ambiente do arquivo .env
load_dotenv()

# Pegando as variáveis de ambiente
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# URL de conexão com o banco de dados PostgreSQL
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criando uma engine assíncrona
engine = create_async_engine(DATABASE_URL, echo=True)

# Criando uma fábrica de sessões assíncronas
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Conexão assíncrona com o banco de dados usando 'databases'
database = Database(DATABASE_URL)


# Dependency: Obter uma sessão de banco de dados assíncrona
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()