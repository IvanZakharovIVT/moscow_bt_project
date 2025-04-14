from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.config import DATABASE_A_URL

engine = create_async_engine(DATABASE_A_URL)

AsyncSessionLocal = async_sessionmaker(bind=engine)

Base = declarative_base()

async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
