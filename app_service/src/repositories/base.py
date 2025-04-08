from abc import ABC, abstractmethod

from pydantic import BaseModel as BaseSchema
from sqlalchemy import update, delete, Update, Delete, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import BaseModel
from src.specifications import Specification, AndSpecification
from src.exceptions import UpdateAllRowsException, DeleteAllRowsException


class BaseRepository(ABC):
    @staticmethod
    @abstractmethod
    async def create(
        session: AsyncSession,
    ) -> BaseModel:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def get(
        session: AsyncSession,
        *specifications: Specification[Select],
        page: int = 1,
        page_size: int = 100,
    ) -> BaseModel:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def update(
        model: BaseModel,
        session: AsyncSession,
        data: BaseSchema,
        *specifications: Specification[Update],
        update_all: bool = False,
    ) -> int:
        if not specifications and not update_all:
            raise UpdateAllRowsException(
                f'You are trying to update all rows from a table {model.__tablename__}. '
                'If you are sure, set update_all to True.'
            )
        statement = update(model).values(**data.model_dump(exclude_unset=True))
        if specifications:
            combined_specifications = AndSpecification(*specifications)
            statement = await combined_specifications.apply_filter(statement)
        execution_result = await session.execute(statement)
        await session.flush()
        if execution_result.supports_sane_rowcount():
            return execution_result.rowcount
        return 1

    @staticmethod
    @abstractmethod
    async def delete(
        model: BaseModel,
        session: AsyncSession,
        *specifications: Specification[Delete],
        delete_all: bool = False,
    ) -> int:
        if not specifications and not delete_all:
            raise DeleteAllRowsException(
                f'You are trying to delete all rows from a table {model.__tablename__}. '
                'If you are sure, set delete_all to True.'
            )
        statement = delete(model)
        if specifications:
            combined_specifications = AndSpecification(*specifications)
            statement = await combined_specifications.apply_filter(statement)
        execution_result = await session.execute(statement)
        await session.flush()
        if execution_result.supports_sane_rowcount():
            return execution_result.rowcount
        return 1
