from datetime import datetime
import uuid

from sqlalchemy import DateTime, Numeric, UUID, VARCHAR, BigInteger, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.models.meta import BaseModel


class RequestModel(BaseModel):
    __tablename__ = 'requests'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text('uuid_generate_v4()'),
    )
    address: Mapped[str] = mapped_column(VARCHAR(42))
    bandwidth: Mapped[int] = mapped_column(BigInteger)
    energy: Mapped[int] = mapped_column(BigInteger)
    balance: Mapped[Numeric] = mapped_column(Numeric(precision=30, scale=6))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
