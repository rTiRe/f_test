from typing import Any

from sqlalchemy.orm import InstrumentedAttribute

from src.specifications.base import T, Specification


class EqualsSpecification(Specification[T]):
    def __init__(self, attribute: InstrumentedAttribute, value: Any) -> None:
        self.attribute = attribute
        self.value = value

    async def apply_filter(self, statement: T) -> T:
        return statement.where(self.attribute == self.value)


class NotEqualsSpecification(EqualsSpecification[T]):
    def __init__(self, attribute: InstrumentedAttribute, value: Any) -> None:
        super().__init__(attribute, value)

    async def apply_filter(self, statement: T) -> T:
        return statement.where(self.attribute != self.value)


class InSpecification(Specification[T]):
    def __init__(self, attribute: InstrumentedAttribute, *values: Any) -> None:
        self.attribute = attribute
        self.values = values

    async def apply_filter(self, statement: T) -> T:
        return statement.where(self.attribute.in_(self.values))
