import pytest_asyncio
from pytest import MonkeyPatch
from unittest.mock import AsyncMock
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from tests.mock.repository import mock_requests
from tests.mock.tron import MockTronService


@pytest_asyncio.fixture(scope='function', autouse=True)
async def get_mock_db(monkeypatch: MonkeyPatch):
    mock_session = AsyncMock(spec=AsyncSession)
    async def mock_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield mock_session
    monkeypatch.setattr('src.storage.postgres.get_db', mock_get_db)
    return mock_session


@pytest_asyncio.fixture(scope='function')
async def get_mock_repository(monkeypatch: MonkeyPatch) -> list[AsyncMock]:
    get_mock = AsyncMock(return_value=mock_requests)
    create_mock = AsyncMock()
    monkeypatch.setattr('src.repositories.RequestRepository.get', get_mock)
    monkeypatch.setattr('src.repositories.RequestRepository.create', create_mock)
    return get_mock, create_mock


@pytest_asyncio.fixture(scope='function')
async def get_mock_tron_service(monkeypatch: MonkeyPatch) -> MockTronService:
    monkeypatch.setattr('src.services.tron.TronService.get_address_info', MockTronService.get_address_info)
    return MockTronService
