from typing import Any, Optional, Type, TypeVar

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.model import BaseORM

T = TypeVar("T", bound=BaseORM)


class BaseRepository[T]:
    """Базовый класс-repository проекта
    для взаимодействия с БД с
    операциями создания, получения, удаления записи
    """

    def __init__(self, model: T, session: AsyncSession):
        """При наследовании обязательно переопределить и указать модель,
        чтобы пользоваться методами класса"""

        self.model = model
        self.session = session


    async def get_any_by(
            self,
            offset: int,
            limit: int,
            order_by="id",
            _desc=True,
            **filters,
    ) -> list[T]:
        """Возвращает отфильтрованный и отсортированый список записей
        по заданным параметрам и фильтрам
       """

        stmt = (select(self.model)
                .filter_by(**filters)
                .offset(offset)
                .limit(limit)
        )

        order_func = getattr(self.model, order_by, None)

        if order_func is not None and _desc:
            stmt = stmt.order_by(desc(order_func))

        result = await self.session.execute(stmt)

        items = result.scalars().all()

        return list(items)

    async def get_one_by(
            self,
            **filters
    ) -> Optional[T]:
        """Возвращает уникальную запись или None по указанным параметрам,
        если > 1 - Ошибка"""

        stmt = select(self.model).filter_by(**filters)
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

        result = await self.get_any_by(offset=0, limit=1, **filters)
        return bool(result)


    async def delete_by_id(
            self,
            item_id: int
    ):
        """Удаляет запись по id"""

        item = await self.get_one_by(id=item_id)
        await self.delete(item)

    async def delete(
            self,
            item: T
    ):
        """Удаляет запись без подтверждения сверху (commit)"""

        await self.session.delete(item)
        await self.session.commit()


    async def get_items_count(self) -> int:
        """Возврвщвет количество записей в таблице"""

        stmt = select(func.count()).select_from(self.model)
        count = await self.session.execute(stmt)
        return count.scalar_one()

    async def update(self, item: T, **updates) -> T:
        for key, value in updates.items():
            setattr(item, key, value)

        return item


    async def search(self, field: str, query: Any, offset: int, limit: int) -> list[T]:
        """Ищет с помощью %reaction% запись"""

        stmt = (select(self.model)
                .where(getattr(self.model, field)
                       .ilike(f"%{query}%"))
                .offset(offset)
                .limit(limit)
                )

        result = await self.session.execute(stmt)

        items = result.scalars().all()

        return list(items)






