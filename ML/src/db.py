from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
import os

load_dotenv()

Base = declarative_base()

engine = create_async_engine(
    url=os.getenv('DB_URL'),
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)
