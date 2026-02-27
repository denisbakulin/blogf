from typing import Any, Optional, TypeVar, Unpack

from base.model import BaseORM
from sqlalchemy import desc, func, or_, select, text, delete
from sqlalchemy.ext.asyncio import AsyncSession
from utils.default import to_dto

T = TypeVar("T", bound=BaseORM)
D = TypeVar("D") #DTO
Q = TypeVar("Q") #Любой sqlalchemy запрос


class BaseRepository[T, D]:
    """Базовый класс-repository проекта
    для взаимодействия с БД с
    операциями создания, получения, удаления записи
    """

    def __init__(self, model: T, session: AsyncSession, dto: type[D]):
        """При наследовании обязательно переопределить и указать модель,
        чтобы пользоваться методами класса"""

        self.model = model
        self.session = session
        self.dto = dto

    def to_dto(self, entity: T) -> D:
        return to_dto(entity, self.dto)


    def paginator(self, stmt: Q,  offset: int | None = None, limit: int | None = None) -> Q:
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
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
            inner_props: dict[str, Any] = None,
            **filters,
    ) -> list[D] | list[Any] | tuple:
        """Возвращает отфильтрованный и отсортированный список записей
        по заданным параметрам и фильтрам
       """

        if lines:
            stmt = select(*[getattr(self.model, i) for i in lines])
        else:
            stmt = select(self.model)

        if filters:
           stmt = self._process_or(stmt=stmt, **filters)

        if inner_props:
            stmt = self._process_stmt_with_inner_fields(inner_props, stmt)

        order_func = getattr(self.model, order_by, None)

        if order_func is not None:
            stmt = stmt.order_by(desc(order_func) if _desc else order_func)

        stmt = self.paginator(stmt)


        result = await self.session.execute(stmt)

        if lines:
            return list(result.all())

        return list(self.to_dto(i) for i in result.scalars().all())


    async def get_orm(
            self,
            inner_props: dict[str, Any] = None,
            **filters
    ) -> Optional[T]:

        stmt = select(self.model)

        stmt = self._process_or(stmt=stmt, **filters)

        stmt = self._process_stmt_with_inner_fields(inner_props, stmt)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()


    async def get_one_by(
            self,
            inner_props: dict[str, Any] = None,
            **filters
    ) -> Optional[D]:
        """Возвращает уникальную запись или None по указанным параметрам,
        если > 1 - Ошибка"""
        result = await self.get_orm(inner_props=inner_props, **filters)

        if result is not None:
            return self.to_dto(result)


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
            delete(self.model).where(id=item_id)
        )


    async def get_items_count(self, **filters) -> int:
        """Возврвщвет количество записей в таблице"""

        stmt = select(func.count()).select_from(self.model)

        if filters:
            stmt = stmt.filter_by(**filters)

        count = await self.session.execute(stmt)
        return count.scalar_one()

    async def update(self, item_id: int, **updates) -> D:
        item = await self.get_orm(id=item_id)

        for key, value in updates.items():
            setattr(item, key, value)

        return self.to_dto(item)


    def _process_stmt_with_inner_fields(self, inner_props: dict[str, Any] | None, stmt: Q) -> Q:
        """
        Добавляет join и фильтры по вложенным свойствам (One-to-One / One-to-Many)
        inner_props = {"settings.show_in_search": True}
        """

        if not inner_props:
            return stmt

        for prop_path, value in inner_props.items():
            parts = prop_path.split(".")
            current_model = self.model
            rel_attr = getattr(current_model, parts[0])

            # join с таблицей
            stmt = stmt.join(rel_attr)

            # проход по вложенным уровням (если есть)
            for part in parts[1:-1]:
                rel_class = rel_attr.property.mapper.class_
                rel_attr = getattr(rel_class, part)
                stmt = stmt.join(rel_attr)

            # фильтр по последнему полю
            rel_class = rel_attr.property.mapper.class_
            column = getattr(rel_class, parts[-1])
            stmt = stmt.where(column == value)

        return stmt






