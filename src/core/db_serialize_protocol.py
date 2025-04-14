from typing import Protocol

from src.core.base_model import BaseDBModel


class DBProtocol(Protocol):
    def get_db_model(self) -> BaseDBModel:
        pass