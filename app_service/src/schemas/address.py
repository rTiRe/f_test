from decimal import Decimal

from pydantic import BaseModel


class AddressInfoRequest(BaseModel):
    address: str


class AddressInfoResponse(BaseModel):
    address: str
    bandwidth: int = 0
    energy: int = 0
    trx_balance: Decimal = 0
