from sqlalchemy import select, Select, Delete, Update
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.base import BaseRepository
from src.models import RequestModel
from src.specifications import Specification, AndSpecification
from src.schemas import RequestSchema, CreateRequestSchema, UpdateRequestSchema


class RequestRepository(BaseRepository):
    @staticmethod
    async def create(
        session: AsyncSession,
        data: CreateRequestSchema,
    ) -> RequestSchema:
        request = RequestModel(**data.model_dump())
        session.add(request)
        await session.flush()
        return RequestSchema(**request.__dict__)

    @staticmethod
    async def get(
        session: AsyncSession,
        *specifications: Specification[Select],
        page: int = 1,
        page_size: int = 100,
    ) -> list[RequestSchema]:
        statement = select(RequestModel)
        if specifications:
            combined_specifications = AndSpecification(*specifications)
            statement = await combined_specifications.apply_filter(statement)
        statement = statement.limit(
            page_size,
        ).offset(
            (page - 1) * page_size,
        ).order_by(
            RequestModel.created_at.desc(),
        )
        requests = (await session.execute(statement)).all()
        return [RequestSchema(**request[0].__dict__) for request in requests]

    @staticmethod
    async def update(
        session: AsyncSession,
        data: UpdateRequestSchema,
        *specifications: Specification[Update],
        update_all: bool = False,
    ) -> int:
        await super(__class__, __class__).update(
            RequestModel,
            session,
            data,
            *specifications,
            update_all=update_all,
        )

    @staticmethod
    async def delete(
        session: AsyncSession,
        *specifications: Specification[Delete],
        delete_all: bool = False,
    ) -> int:
        await super(__class__, __class__).delete(
            RequestModel,
            session,
            *specifications,
            delete_all=delete_all,
        )
