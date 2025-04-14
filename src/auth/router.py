from datetime import timedelta
from typing import Annotated

from fastapi.security import HTTPBasicCredentials

from src.core.security import token_security, basic_security, access_security, refresh_security, get_token_from_request
from fastapi import APIRouter, Depends, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession


from src.auth.config import REFRESH_TOKEN_TIMEDELTA, AUTH_TOKEN_TIMEDELTA
from src.auth.repository import UserRepository
from src.auth.schema import UserBase
from src.core.utils.user_auth_utils import authenticate_and_get_user_jwt, authenticate_and_get_user
from src.database.db_config import get_session

router = APIRouter(tags=['auth'])


@router.get(
    '/user/me',
    summary='Получение данных пользователя',
    description='Получение данных пользователя',
    response_model=UserBase
)
async def get_user_me(
        user_id: int,
        credentials: Annotated[dict, Depends(token_security)],
        session: AsyncSession = Depends(get_session),
):
    user = await authenticate_and_get_user_jwt(credentials.get('username'), session)
    return await UserRepository(session).get_by_id(user_id)


@router.post("/auth")
async def auth(
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_security)],
        session: AsyncSession = Depends(get_session),
):
    user = await authenticate_and_get_user(credentials.username, credentials.password, session)

    subject = {"username": user.username, "id": user.id, "user_type": user.user_type}
    return {
        "access_token": access_security.create_access_token(
            subject=subject,
            expires_delta=timedelta(minutes=AUTH_TOKEN_TIMEDELTA)
        ),
        "refresh_token": refresh_security.create_refresh_token(
            subject=subject,
            expires_delta=timedelta(minutes=REFRESH_TOKEN_TIMEDELTA)
        ),
    }

@router.post("/refresh")
async def refresh_token(
    token: Annotated[dict, Depends(refresh_security)],
):
    return {
        "access_token": access_security.create_access_token(
            subject=token.subject,
            expires_delta = timedelta(minutes=AUTH_TOKEN_TIMEDELTA)
        )
    }

@router.post("/auth_cookie")
async def auth_cookie(
        response: Response,
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_security)],
        session: AsyncSession = Depends(get_session),
):
    user = await authenticate_and_get_user(credentials.username, credentials.password, session)

    subject = {"username": user.username, "id": user.id, "user_type": user.user_type}
    auth_token = access_security.create_access_token(
        subject=subject,
        expires_delta=timedelta(minutes=AUTH_TOKEN_TIMEDELTA)
    )
    refresh_token_val = refresh_security.create_refresh_token(
        subject=subject,
        expires_delta=timedelta(minutes=REFRESH_TOKEN_TIMEDELTA)
    )
    response.set_cookie(
        key="access_token",
        value=auth_token,
        httponly=True,
        max_age=AUTH_TOKEN_TIMEDELTA*60,  # 30 минут
        secure=True,  # Только для HTTPS
        samesite="lax"
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token_val,
        httponly=True,
        max_age=REFRESH_TOKEN_TIMEDELTA*60,  # 30 минут
        secure=True,  # Только для HTTPS
        samesite="lax"
    )
    return {"message": "Successfully logged in"}

@router.get("/protected")
async def protected_route(token: str = Depends(get_token_from_request)):
    # Доступно только с валидным токеном
    return {"message": "Protected data", "user": token}
