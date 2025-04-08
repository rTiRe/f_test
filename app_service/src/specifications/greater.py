from typing import Any

from sqlalchemy.orm import InstrumentedAttribute

from src.specifications.base import T, Specification


class GreaterThanSpecification(Specification[T]):
    def __init__(self, attribute: InstrumentedAttribute, value: Any) -> None:
        self.attribute = attribute
        self.value = value

    async def apply_filter(self, statement: T) -> T:
        return statement.where(self.attribute > self.value)


class GreaterEqualsSpecification(GreaterThanSpecification[T]):
    def __init__(self, attribute: InstrumentedAttribute, value: Any) -> None:
        super().__init__(attribute, value)

    async def apply_filter(self, statement: T) -> T:
        return statement.where(self.attribute >= self.value)
