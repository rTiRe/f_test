import pytest_asyncio
from pytest import MonkeyPatch

from tests.mock.tron import MockTronService


@pytest_asyncio.fixture(scope='function', autouse=True)
async def get_mock_tron_service(monkeypatch: MonkeyPatch) -> MockTronService:
    monkeypatch.setattr('src.services.tron.TronService.get_address_info', MockTronService.get_address_info)
    return MockTronService
