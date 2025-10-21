import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL", "mysql+aiomysql://root:secret@127.0.0.1:3306/bdu_inventory")

engine = create_async_engine(DB_URL, echo=False, pool_pre_ping=True, future=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
