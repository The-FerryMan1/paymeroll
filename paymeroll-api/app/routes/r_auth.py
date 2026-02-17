from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.auth import (
    admin_check,
    create_access_token,
    hash_password,
    oauth2_scheme,
    verify_access_token,
    verify_password,
)
from app.core.config import settings
from app.dependencies import get_db
from app.models.user import User
from app.schemas.s_user import Token, UserCreate, UserResponsePrivate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/create_user",
    response_model=UserResponsePrivate,
    status_code=201,
    dependencies=[Depends(admin_check)],
)
async def create_user(
    user: UserCreate, db: Annotated[AsyncSession, Depends(get_db.getDB)]
):
    result = await db.execute(
        select(User).where(func.lower(User.username) == user.username.lower())
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    new_user = User(
        username=user.username,
        full_name=user.full_name,
        email=user.email.lower(),
        contact_no=user.contact_no,
        hashed_password=hash_password(user.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
async def login(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db.getDB)],
):
    result = await db.execute(
        select(User).where(func.lower(User.email) == credentials.username.lower())
    )

    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password or username",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponsePrivate)
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db.getDB)],
):
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user_id_int = int(user_id)  # type: ignore
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(select(User).where(User.id == user_id_int))

    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
