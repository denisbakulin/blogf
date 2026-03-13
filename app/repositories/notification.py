from base.repository import BaseRepository
from entities.notification import Notification
from sqlalchemy.ext.asyncio import AsyncSession


class NotificationRepository(BaseRepository[Notification]):

    def __init__(self, session: AsyncSession):
        super().__init__(Notification, session)





