from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import UserAuthorizationError
from src.auth.repository import UserRepository


async def authenticate_and_get_user(username: str, password: str, session: AsyncSession):
    user = await UserRepository(session).authenticate_user(username, password)

    return user


async def authenticate_and_get_user_jwt(username: str, session: AsyncSession):
    user = await UserRepository(session).get_user_by_username(username)
    if not user:
        raise UserAuthorizationError(username)

    return user
