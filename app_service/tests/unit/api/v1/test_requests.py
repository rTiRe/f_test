import pytest
from unittest.mock import AsyncMock

from src.api.v1.requests import get_requests
from src.schemas import RequestSchema
from src.repositories.request import RequestRepository
from tests.mock.repository import mock_requests


@pytest.mark.asyncio
async def test_get_requests(get_mock_db: AsyncMock, get_mock_repository: AsyncMock) -> None:
    result = await get_requests(page=1, page_size=100)
    assert result == mock_requests
    assert isinstance(result[0], RequestSchema)
    RequestRepository.get.assert_awaited_once_with(get_mock_db, page=1, page_size=100)
