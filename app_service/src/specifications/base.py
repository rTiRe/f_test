from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from sqlalchemy import Select, Update, Delete
from sqlalchemy.sql import or_, not_


T = TypeVar('T', Select, Update, Delete)


class Specification(ABC, Generic[T]):
    @abstractmethod
    async def apply_filter(self, statement: T) -> T:
        raise NotImplementedError()

    def __and__(self, other: 'Specification[T]') -> 'AndSpecification[T]':
        return AndSpecification(self, other)

    def __or__(self, other: 'Specification[T]') -> 'OrSpecification[T]':
        return OrSpecification(self, other)

    def __invert__(self) -> 'NotSpecification[T]':
        return NotSpecification(self)

    def __neg__(self) -> 'NotSpecification[T]':
        return NotSpecification(self)


class AndSpecification(Specification[T]):
    def __init__(self, *specifications: Specification[T]) -> None:
        self.specifications = specifications

    async def apply_filter(self, statement: T) -> T:
        for spec in self.specifications:
            statement = await spec.apply_filter(statement)
        return statement


class OrSpecification(Specification[T]):
    def __init__(self, *specifications: Specification[T]) -> None:
        self.specifications = specifications

    async def apply_filter(self, statement: T) -> T:
        conditions = []
        for spec in self.specifications:
            conditions.append((await spec.apply_filter(statement)).whereclause)
        return statement.where(or_(*conditions))


class NotSpecification(Specification[T]):
    def __init__(self, specification: Specification[T]) -> None:
        self.specification = specification

    async def apply_filter(self, statement: T) -> T:
        condition = (await self.specification.apply_filter(statement)).whereclause
        return statement.where(not_(condition))
