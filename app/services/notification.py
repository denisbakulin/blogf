from base.service import BaseService
from entities import Notification, NotificationType
from repositories import NotificationRepository
from sqlalchemy.ext.asyncio import AsyncSession


class NotificationService(BaseService[Notification, NotificationRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Notification, session, NotificationRepository)


    async def process(self, user_id: int, type_: NotificationType):
        n = await self.repository.get_one_by(user_id=user_id, type=type_)
        if n is None:
            await self.create_item(user_id=user_id, type=type_)
        else:
            await self.delete_item_by_id(n.id)


