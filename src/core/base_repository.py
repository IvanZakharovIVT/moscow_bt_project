from abc import abstractmethod
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


from src.core.base_model import BaseDBModel
from src.core.db_serialize_protocol import DBProtocol


class BaseRepository:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, unit_id: int) -> BaseDBModel:
        request = await self._get_by_id(unit_id)
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return request

    async def get_all(self) -> Sequence[BaseDBModel]:
        select_request = self._get_all_select()
        result = await self._session.execute(select_request)
        return result.scalars().all()

    async def create(self, request: DBProtocol) -> BaseDBModel:
        model = request.get_db_model()
        self._session.add(model)
        await self.flush()
        return model

    @abstractmethod
    async def _get_by_id(self, unit_id: int) -> BaseDBModel:
        raise NotImplementedError

    @abstractmethod
    def _get_all_select(self) -> Select:
        raise NotImplementedError

    async def commit(self):
        await self._session.commit()

    async def flush(self):
        await self._session.flush()
