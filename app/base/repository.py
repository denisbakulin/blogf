from typing import Any, TypeVar

from base.model import BaseORM
from sqlalchemy import Select, delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=BaseORM)


class BaseRepository[T]:
    """Базовый класс-repository проекта
    для взаимодействия с БД с
    операциями создания, получения, удаления записи
    """

    def __init__(self, model: T, session: AsyncSession):
        """При наследовании обязательно переопределить и указать модель,
        DTO представление"""

        self.model = model
        self.session = session


    def process_paginate_stmt(
            self, stmt: Select,
            offset: int | None = None,
            limit: int | None = None
    ) -> Select:

        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        return stmt

    def process_search_stmt(
            self, stmt: Select,
            strict: bool,
            field: str,
            value: Any
    ) -> Select:

        column = getattr(self.model, field)

        if strict:
            stmt = stmt.where(column == value)
        else:
            stmt = stmt.where(column.ilike(f"%{value}%"))
        return stmt


    def _process_or(self, stmt, **filters):
        for key, value in filters.items():
            column = getattr(self.model, key)
            if isinstance(value, list):
                stmt = stmt.where(column.in_(value))
            else:
                stmt = stmt.where(column == value)
        return stmt

    async def get_any_by(
            self,
            offset: int | None = None,
            limit: int | None = None,
            lines: list | None = None,
            order_by: str = "id",
            _desc: bool = True,
            **filters,
    ) -> list[T] | list[Any] | tuple:
        """Возвращает отфильтрованный и отсортированный список записей
        по заданным параметрам и фильтрам
       """


        stmt = select(self.model)

        stmt = self._process_or(stmt=stmt, **filters)

        order_func = getattr(self.model, order_by, None)

        if order_func is not None:
            stmt = stmt.order_by(desc(order_func) if _desc else order_func)

        stmt = self.process_paginate_stmt(stmt, offset, limit)

        result = await self.session.execute(stmt)

        if lines:
            return list(result.all())

        return list(i for i in result.scalars().all())


    async def search(
            self,
            offset: int | None = None,
            limit: int | None = None,
            lines: list | None = None,
            order_by: str = "id",
    ):
        ...
        """НАдо прописать"""


    async def get_one_by(
            self, **filters
    ) -> T | None:
        """Возвращает уникальную запись или None по указанным параметрам,
        если > 1 - Ошибка"""
        stmt = self._process_or(stmt=select(self.model), **filters)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()


    def create(
            self,
            **data
    ) -> T:
        """Создает запись"""

        item = self.model(**data)
        self.session.add(item)
        return item


    async def exists(
            self,
            **filters
    ) -> bool:
        """Проверяет существование записи"""

        result = await self.get_any_by(**filters)
        return bool(result)


    async def delete_by_id(
            self,
            item_id: int
    ):
        """Удаляет запись по id"""

        await self.session.execute(
            delete(self.model).where(self.model.id == item_id)
        )


    async def get_items_count(self, **filters) -> int:
        """Возвращает количество записей в таблице"""

        stmt = select(func.count()).select_from(self.model).filter_by(**filters)

        count = await self.session.execute(stmt)
        return count.scalar_one()

    async def update(self, item_id: int, **updates) -> T:
        item = await self.get_one_by(id=item_id)

        for key, value in updates.items():
            setattr(item, key, value)

        return item




