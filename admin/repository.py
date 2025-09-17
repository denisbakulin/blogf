from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, func


class AdminRepository[T]:

    def __init__(self, session: AsyncSession, model: T):
        self.session = session
        self.model = model

    async def get_item_by_id(self, item_id) -> T:
        return await self.session.get(self.model, item_id)

    async def get_items_count(self) -> int:
        stmt = select(func.count()).select_from(self.model)
        count = await self.session.execute(stmt)
        return count.scalar_one()

    async def create_item(self, item_data: dict) -> T:
        item = self.model(**item_data)
        self.session.add(item)
        return item

    async def update_item(self, item: T, update_data: dict) -> T:
        for field, value in update_data.items():
            setattr(item, field, value)
        return item

    async def delete_item(self, item_id):
        stmt = delete(self.model).where(self.model.id == item_id)
        await self.session.execute(stmt)


