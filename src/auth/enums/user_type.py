from functools import cached_property

from src.core.described_enum import DescribedEnum


class UserType(str, DescribedEnum):
    ADMIN = "admin"
    VIEWER = "viewer"

    @cached_property
    def _description_items(self) -> dict:
        return {
            self.ADMIN: 'Админ',
            self.VIEWER: 'Наблюдатель'
        }
