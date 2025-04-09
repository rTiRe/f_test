from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider
from tronpy.exceptions import AddressNotFound

from config import settings
from src.schemas import AddressInfoResponseSchema


class TronService:
    def __init__(self):
        self.client = AsyncTron(
            provider=AsyncHTTPProvider(
                api_key=settings.TRON_API_KEY.get_secret_value(),
            ),
        )

    async def get_address_info(self, address: str) -> AddressInfoResponseSchema:
        if not self.client.is_address(address):
            raise AddressNotFound(f'Invalid Tron address {address}')
        account = await self.client.get_account(address)
        bandwith = await self.client.get_bandwidth(address)
        resource = await self.client.get_account_resource(address)
        energy_used = resource.get('EnergyUsed', 0)
        energy_limit = resource.get('EnergyLimit', 0)
        energy_available = energy_limit - energy_used
        return AddressInfoResponseSchema(
            address=address,
            bandwidth=bandwith,
            energy=energy_available,
            trx_balance=account.get('balance', 0) / 1_000_000
        )
