from geoalchemy2 import Geometry
from sqlalchemy import Column, String, Integer, Index

from src.core.base_model import BaseDBModel


class User(BaseDBModel):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}

    username = Column(String(), index=True, unique=True)
    user_type = Column(String(20))
    password = Column(String(255))


class Location(BaseDBModel):
    __tablename__ = 'locations'
    __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True)
    geom = Column(Geometry('POINT', srid=4326, spatial_index=False))
