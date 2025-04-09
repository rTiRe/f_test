from fastapi import Query

from src.api.v1.router import router
from src.schemas import RequestSchema
from src.storage.postgres import get_db
from src.repositories import RequestRepository


@router.get('/requests', response_model=list[RequestSchema])
async def get_requests(
    page: int = Query(1, ge=0),
    page_size: int = Query(100, le=250),
) -> list[RequestSchema]:
    async for db in get_db():
        return await RequestRepository.get(db, page=page, page_size=page_size)
