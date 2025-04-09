import pytest
from unittest.mock import AsyncMock

from src.api.v1.tron.address import get_address_info
from src.schemas import AddressInfoRequestSchema, AddressInfoResponseSchema
from tests.mock.repository import mock_requests, MockRequestRepository
from tests.mock.tron import MockTronService


@pytest.mark.asyncio
async def test_address_requests(
    get_mock_db: AsyncMock,
    get_mock_repository: MockRequestRepository,
    get_mock_tron_service: MockTronService,
) -> None:
    address = 'Tabc'
    result = await get_address_info(AddressInfoRequestSchema(address=address))
    assert isinstance(result, AddressInfoResponseSchema)
    assert result.address == address
