import json

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete

from src.storage.postgres import get_db
from src.models.request import RequestModel
from src.schemas import RequestSchema
from src.__main__ import create_app



@pytest.mark.asyncio(loop_scope='session')
async def test_get_requests():
    request_models = [
            RequestModel(
                address='Tabc',
                bandwidth=600,
                energy=1,
                trx_balance=123,
            ),
            RequestModel(
                address='Tcba',
                bandwidth=599,
                energy=2,
                trx_balance=321,
            ),
        ]
    async for db in get_db():
        db.add_all(request_models)
        await db.commit()
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url='http://test',
    ) as client:
        response = await client.get('/api/v1/requests', params={'page': 1, 'page_size': 100})
    async for db in get_db():
        await db.execute(delete(RequestModel))
        await db.commit()
    response_content = json.loads(response.content)
    assert response.status_code == 200
    assert len(response_content) == 2
    assert RequestSchema(**response_content[0])
