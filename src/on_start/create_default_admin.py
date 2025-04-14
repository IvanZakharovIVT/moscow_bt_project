from src.auth.models import User
from src.auth.repository import UserRepository
from src.auth.utils import hash_password

from src.config import DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD


async def create_admin_user(db_session):
    username = DEFAULT_ADMIN_USERNAME
    existed_user = await UserRepository(db_session).get_user_by_username(username)
    if not existed_user:
        password = hash_password(DEFAULT_ADMIN_PASSWORD)
        user = User(
            username=username,
            user_type="admin",
            password=password,
        )
        db_session.add(user)
