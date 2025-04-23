from __future__ import annotations

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.core.base_model import BaseDBModel


class User(BaseDBModel):
    __tablename__ = 'users'

    username = Column(String(), index=True, unique=True)
    user_type = Column(String(20))
    password = Column(String(255))
    telegram_id = Column(String(20))
    notification = relationship("Notification", back_populates="user", lazy="subquery")
    # bt_place = relationship("BTPlace", back_populates="user", lazy="subquery")


class Notification(BaseDBModel):
    __tablename__ = 'notification'

    status = Column(String(20))
    body = Column(String(255))
    user_id = Column(Integer, ForeignKey(User.id, ondelete="SET NULL"), nullable=True)
    user = relationship('User', foreign_keys='Notification.user_id')
