from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.enums.user_type import UserType
from src.auth.exceptions import UserAuthorizationError
from src.auth.models import User
from src.auth.repository import UserRepository


async def authenticate_and_get_user(username: str, password: str, session: AsyncSession):
    user = await UserRepository(session).authenticate_user(username, password)

    return user


async def authenticate_and_get_user_jwt(username: str, session: AsyncSession):
    user = await UserRepository(session).get_user_by_username(username)
    if not user:
        raise UserAuthorizationError(username)

    return user

async def check_user_permissions(user: User, allowed_user_types: list[UserType]):
    if user.user_type not in allowed_user_types:
        allowed_roles = ', '.join([v.description for v in allowed_user_types])
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Недостаточно прав. Доступно только для {allowed_roles}")
