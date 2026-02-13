from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
SQL_DATABASE_URL = "sqlite+aiosqlite:///./payroll.db"

engine = create_async_engine(SQL_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass
