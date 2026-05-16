from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar("ModelT")


class AbstractRepository(ABC, Generic[ModelT]):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> ModelT | None: ...

    @abstractmethod
    async def save(self, entity: ModelT) -> ModelT: ...

    @abstractmethod
    async def delete(self, id: UUID) -> bool: ...


class SQLAlchemyRepository(AbstractRepository[ModelT]):
    def __init__(self, session: AsyncSession, model_class: type[ModelT]) -> None:
        self._session = session
        self._model = model_class

    async def get_by_id(self, id: UUID) -> ModelT | None:
        return await self._session.get(self._model, id)

    async def get_by(self, **filters: Any) -> ModelT | None:
        stmt = select(self._model)
        for attr, value in filters.items():
            stmt = stmt.where(getattr(self._model, attr) == value)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by(self, **filters: Any) -> list[ModelT]:
        stmt = select(self._model)
        for attr, value in filters.items():
            stmt = stmt.where(getattr(self._model, attr) == value)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def save(self, entity: ModelT) -> ModelT:
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def delete(self, id: UUID) -> bool:
        entity = await self.get_by_id(id)
        if entity is None:
            return False
        await self._session.delete(entity)
        return True
