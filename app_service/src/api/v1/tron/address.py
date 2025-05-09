from fastapi import HTTPException, status
from tronpy.exceptions import AddressNotFound

from src.api.v1.tron.router import router
from src.schemas import AddressInfoRequestSchema, AddressInfoResponseSchema
from src.services import TronService
from src.storage import postgres
from src.repositories import RequestRepository
from src.schemas import CreateRequestSchema


@router.post('/address', response_model=AddressInfoResponseSchema)
async def get_address_info(request: AddressInfoRequestSchema) -> AddressInfoResponseSchema:
    tron_service = TronService()
    try:
        address_info = await tron_service.get_address_info(request.address)
    except AddressNotFound as exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exception))
    except Exception as exception:
        raise HTTPException(
            status_code=500,
            detail=f'Error fetching data: {str(exception)}',
        )
    async for db in postgres.get_db():
        await RequestRepository.create(db, CreateRequestSchema(**address_info.model_dump()))
        await db.commit()
    return address_info
