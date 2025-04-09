from unittest.mock import AsyncMock

from tronpy.exceptions import AddressNotFound

from src.schemas import AddressInfoResponseSchema


class MockTronService:
    def __init__(self):
        self.client = AsyncMock()

    async def get_address_info(self, address: str) -> AddressInfoResponseSchema:
        if not address.startswith('T'):
            raise AddressNotFound(f'Invalid Tron address {address}')
        return AddressInfoResponseSchema(
            address=address,
            bandwidth=600,
            energy=1,
            trx_balance=123,
        )
