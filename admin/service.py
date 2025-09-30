from sqlalchemy.ext.asyncio import AsyncSession
from core.service import BaseService
from core.repository import BaseRepository


class AdminService[T](BaseService):
    def __init__(self, model: T, session: AsyncSession):
        super().__init__(model, session)
        self.repository = BaseRepository(model, session)


    async def get_items_count(self) -> int:
        return await self.repository.get_items_count()








