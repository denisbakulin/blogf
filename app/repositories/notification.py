from sqlalchemy.ext.asyncio import AsyncSession

from base.repository import BaseRepository
from entities.notification import Notification


class NotificationRepository(BaseRepository[Notification]):

    def __init__(self, session: AsyncSession):
        super().__init__(Notification, session)





