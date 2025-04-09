from decimal import Decimal

from pydantic import BaseModel


class AddressInfoRequestSchema(BaseModel):
    address: str


class AddressInfoResponseSchema(BaseModel):
    address: str
    bandwidth: int = 0
    energy: int = 0
    trx_balance: Decimal = 0
