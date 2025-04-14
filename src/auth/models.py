from sqlalchemy import Column, String

from src.core.base_model import BaseDBModel


class User(BaseDBModel):
    __tablename__ = 'users'

    username = Column(String(), index=True, unique=True)
    user_type = Column(String(20))
    password = Column(String(255))