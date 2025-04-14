from typing import Sequence

from sqlalchemy import select, Select

from src.auth.exceptions import UserAuthorizationError
from src.auth.models import User
from src.auth.schema import UserBase
from src.auth.utils import hash_password
from src.core.base_repository import BaseRepository


class UserRepository(BaseRepository):

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self._session.execute(select(User).filter_by(username=username))
        return result.scalar_one_or_none()

    async def authenticate_user(self, username: str, password: str) -> User:
        password = hash_password(password)
        user = await self.get_user_by_username(username)
        if user and user.password == password:
            return user
        raise UserAuthorizationError(username)

    async def change_user_password(self, user_for_change: User, new_password: str):
        user_for_change.password = new_password
        self._session.add(user_for_change)
        await self._session.flush()

    async def get_non_admin_users(self) -> Sequence[User]:
        base_select = self._get_all_select()
        result = await self._session.execute(
            base_select.filter(User.user_type != "admin")
        )
        return result.scalars().all()

    def _get_all_select(self) -> Select:
        return select(User).order_by(User.id.desc())

    async def add_new_user(self, user: UserBase, new_username: str, new_password: str) -> User:
        new_user = user.get_db_model()
        new_user.username = new_username
        new_user.password = new_password
        self._session.add(new_user)
        await self._session.flush()
        return new_user

    async def _get_by_id(self, unit_id: int) -> User:
        user: User | None = await self._session.get(User, unit_id)
        return user
