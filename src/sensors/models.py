from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.core.base_model import BaseDBModel


class Sensor(BaseDBModel):
    __tablename__ = 'sensor'
    bt_session = relationship("Stats", back_populates="sensor", lazy="subquery")



class Stats(BaseDBModel):
    __tablename__ = 'stats'
    sensor_id = Column(Integer, ForeignKey(Sensor.id, ondelete="SET NULL"), nullable=True)
    sensor = relationship('Sensor', foreign_keys='Stats.sensor_id')
