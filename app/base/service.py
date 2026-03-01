from typing import Any, TypeVar

from base.exceptions import (EntityAlreadyExists, EntityBadRequestError,
                             EntityNotFoundError)
from base.model import BaseORM
from base.repository import BaseRepository
from helpers.search import Pagination
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=BaseORM)
R = TypeVar("R", bound=BaseRepository)


class BaseService[T, R]:
    """
    Базовый класс-service проекта
    с бизнес-логикой для crud объектов
    """

    def __init__(
            self,
            model: T,
            session: AsyncSession,
            repository: type[R]
    ):
        """При наследовании обязательно переопределить и указать модель,
        чтобы пользоваться методами класса"""

        self.model = model
        self.session = session
        self.repository: R = repository(session=session)




    async def create_item(self, **params) -> T:
        item = self.repository.create(**params)

        await self.session.commit()
        await self.session.refresh(item)

        return item


    async def get_by_or_raise(self, **params) -> T:
        """
        Возвращает запись по совпадениям params

        :raise
            EntityNotFoundError: Если запись не найдена
        """
        try:
            item = await self.repository.get_one_by(**params)
            if not item:
                raise EntityNotFoundError(
                    self.model.__name__,
                    **params
                )
            return item
        except SQLAlchemyError:
            raise EntityBadRequestError(
                entity=self.model.__name__, message="Больше 1 объекта в базе"
            )

    async def get_item_by_id(self, item_id: int) -> T:
        return await self.get_by_or_raise(id=item_id)

    async def get_items_by(
            self,
            pagination: Pagination,
            **params
    ) -> list[T]:
        return await self.repository.get_any_by(**params, **pagination.dict())



    async def check_already_exists(self, **fields):
        """
        Проверяет на существование записи

        :raise
            EntityAlreadyExists: Если запись существует
        """

        item = await self.repository.exists(**fields)

        if item:
            raise EntityAlreadyExists(
                entity=self.model.__name__,
                **fields
            )



    async def delete_item_by_id(self, item_id):
        """Удаляет запись по переданному id"""

        await self.repository.delete_by_id(item_id)



    async def update_item(self, item_id: int, **updates) -> T:
        item = await self.get_item_by_id(item_id)

        await self.repository.update(item_id, **updates)
        await self.session.commit()
        await self.session.refresh(item)

        return item

    async def search_items(
            self,
            search,
            pagination: Pagination,
            inner_props: dict[str, Any] | None = None,
            **filters,
    ) -> list[T]:

        if search.strict:
            return await self.repository.get_any_by(
                **{search.field: search.q},
                **pagination.dict(),
                **filters,
                inner_props=inner_props,

            )
        return await self.repository.search(
            field=search.field,
            query=search.q,
            **pagination.dict(),
            **filters,
            inner_props=inner_props,
        )

