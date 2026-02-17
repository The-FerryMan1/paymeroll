from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

SQL_DATABASE_URL = "sqlite+aiosqlite:///./payroll.db"

engine = create_async_engine(
    SQL_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


async def seed_data(db: AsyncSession):
    from sqlalchemy import select

    from app.core.auth import hash_password
    from app.models.user import User

    user = await db.execute(select(User).where(User.role == "admin"))
    user = user.scalar_one_or_none()

    if not user:
        seed_user = User(
            username="admin",
            full_name="Admin User",
            email="admin@example.com",
            contact_no="1234567890",
            hashed_password=hash_password("password123"),
            role="admin",
            is_active=True,
        )
        db.add(seed_user)
        await db.commit()
        await db.refresh(seed_user)
    else:
        print("Admin user already exists")
