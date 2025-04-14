from datetime import datetime, timezone

from sqlalchemy import Column, func, Integer, TIMESTAMP
from sqlalchemy.orm import validates

from src.database.db_config import Base


class BaseDBModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=func.now(),
                        nullable=False)

    modified_at = Column(TIMESTAMP(timezone=True),
                         server_default=func.now(),
                         onupdate=func.now(),
                         nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    @validates('created_at')
    def validate_created_at(self, key, value):
        return value.replace(tzinfo=timezone.utc)

    @validates('modified_at')
    def validate_modified_at(self, key, value):
        return value.replace(tzinfo=timezone.utc)