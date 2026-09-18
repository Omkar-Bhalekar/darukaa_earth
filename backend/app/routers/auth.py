from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.jwt import create_access_token, create_refresh_token, decode_token
from app.auth.security import hash_password, verify_password
from app.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="none" if settings.COOKIE_SECURE else "lax",
        secure=settings.COOKIE_SECURE,
        path="/",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="none" if settings.COOKIE_SECURE else "lax",
        secure=settings.COOKIE_SECURE,
        path="/",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )


@router.post("/register", response_model=UserResponse)
async def register(
    user_in: UserCreate, response: Response, db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(User).filter(User.email == user_in.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_pwd = hash_password(user_in.password)
        new_user = User(
            email=user_in.email, hashed_password=hashed_pwd, name=user_in.name
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except HTTPException:
        raise
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is unavailable. Try again shortly.",
        ) from exc

    access_token = create_access_token(new_user.id)
    refresh_token = create_refresh_token(new_user.id)
    set_auth_cookies(response, access_token, refresh_token)
    return new_user


@router.post("/login", response_model=UserResponse)
async def login(
    user_in: UserLogin, response: Response, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).filter(User.email == user_in.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    set_auth_cookies(response, access_token, refresh_token)
    return user


@router.post("/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token"
        )
    try:
        user_id = decode_token(refresh_token)
        access_token = create_access_token(user_id)
        new_refresh_token = create_refresh_token(user_id)
        set_auth_cookies(response, access_token, new_refresh_token)
        return {"detail": "Token refreshed"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        samesite="none" if settings.COOKIE_SECURE else "lax",
        secure=settings.COOKIE_SECURE,
    )
    response.delete_cookie(
        key="refresh_token",
        path="/",
        samesite="none" if settings.COOKIE_SECURE else "lax",
        secure=settings.COOKIE_SECURE,
    )
    return {"detail": "Logged out"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
