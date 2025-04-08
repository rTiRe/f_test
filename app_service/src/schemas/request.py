from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class RequestSchema(BaseModel):
    id: UUID
    address: str
    bandwidth: int
    energy: int
    balance: Decimal
    created_at: datetime


class CreateRequestSchema(BaseModel):
    address: str
    bandwidth: int
    energy: int
    balance: Decimal


class UpdateRequestSchema(BaseModel):
    address: str | None = None
    bandwidth: int | None = None
    energy: int | None = None
    balance: Decimal | None = None
