from __future__ import annotations

from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from src.auth.models import User
from src.core.base_model import BaseDBModel


class BTPlace(BaseDBModel):
    __tablename__ = 'bt_place'

    imei = Column(String(15), index=True, unique=True)
    bt_session = relationship("BTSessions", back_populates="bt", lazy="subquery")
    user_id = Column(Integer, ForeignKey(User.id, ondelete="SET NULL"), nullable=True)
    user = relationship('User', foreign_keys='BTPlace.user_id')

class BTSessions(BaseDBModel):
    __tablename__ = 'bt_session'

    bt_id = Column(Integer, ForeignKey(BTPlace.id, ondelete="SET NULL"), nullable=True)
    bt = relationship('BTPlace', foreign_keys='BTSessions.bt_id')
    end_session_time = Column(TIMESTAMP(timezone=True), nullable=True)
    bt_usage = relationship("BTUsage", back_populates="bt_session", lazy="subquery")


class BTUsage(BaseDBModel):
    __tablename__ = 'bt_usage'

    bt_session_id = Column(Integer, ForeignKey(BTSessions.id, ondelete="SET NULL"), nullable=True)
    bt_session = relationship('BTSessions', foreign_keys='BTUsage.bt_session_id')