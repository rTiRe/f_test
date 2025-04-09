from datetime import datetime
from uuid import uuid4
from unittest.mock import AsyncMock

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.specifications import Specification
from src.schemas import RequestSchema


mock_requests = [
    RequestSchema(
        id=uuid4(),
        address='test1',
        bandwidth=600,
        energy=1,
        trx_balance=123,
        created_at=datetime.now(),
    ),
    RequestSchema(
        id=uuid4(),
        address='test2',
        bandwidth=599,
        energy=2,
        trx_balance=321,
        created_at=datetime.now(),
    ),
]


class MockRequestRepository:
    @staticmethod
    async def get(
        session: AsyncSession,
        *specifications: Specification[Select],
        page: int = 1,
        page_size: int = 100,
    ) -> list[RequestSchema]:
        return mock_requests[page_size*(page-1):page_size*page]


mock_repository = MockRequestRepository()
