import abc
from enum import Enum
from functools import cached_property


class DescribedEnum(Enum):

    @property
    def description(self) -> str:
        return self._description_items.get(self)

    @cached_property
    @abc.abstractmethod
    def _description_items(self) -> dict:
        raise NotImplementedError
