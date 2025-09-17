from sqlalchemy.ext.asyncio import AsyncSession

from admin.repository import AdminRepository
from core.exceptions import EntityNotFoundError


class AdminService[T]:
    def __init__(self, model: T, session: AsyncSession):
        self.repo = AdminRepository[T](session=session, model=model)
        self.model = model
        self.session = session

    async def get_item_by_id(self, item_id: int) -> T:
        item = await self.repo.get_item_by_id(item_id)

        if not item:
            raise EntityNotFoundError(
                str(self.model.__name__),
                item_id
            )

        return item

    async def get_items_count(self) -> int:
        return await self.repo.get_items_count()

    async def create_item(self, item_create) -> T:

        item = await self.repo.create_item(item_create.model_dump())

        await self.session.commit()
        await self.session.refresh(item)

        return item




    async def update_item(self, item_id: int, update_info) -> T:

        item = await self.get_item_by_id(item_id)

        await self.repo.update_item(item, update_info.model_dump(exclude_none=True))

        await self.session.commit()
        await self.session.refresh(item)

        return item



    async def delete_item(self, item_id: int):
        await self.repo.delete_item(item_id)

        await self.session.commit()




