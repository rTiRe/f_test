import json

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete, select

from src.storage.postgres import get_db
from src.models.request import RequestModel
from src.schemas import AddressInfoRequestSchema, AddressInfoResponseSchema
from src.__main__ import create_app



@pytest.mark.asyncio(loop_scope='session')
async def test_get_address_info():
    test_address = 'Tabc'
    request_data = AddressInfoRequestSchema(
        address=test_address,
    )
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url='http://test',
    ) as client:
        response = await client.post('/api/v1/tron/address', json=request_data.model_dump())
    async for db in get_db():
        requests = (await db.execute(select(RequestModel))).all()
        assert len(requests) == 1
        assert requests[0][0].address == test_address
        await db.execute(delete(RequestModel))
        await db.commit()
    response_content = json.loads(response.content)
    assert response.status_code == 200
    assert AddressInfoResponseSchema(**response_content)
    assert response_content['address'] == test_address
