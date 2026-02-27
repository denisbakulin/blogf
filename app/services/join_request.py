from base.service import BaseService
from models.container import Container
from models.join_request import JoinRequest
from repositories.join_request import JoinRequestRepository
from sqlalchemy.ext.asyncio import AsyncSession
from user import User


class JoinRequestService(BaseService[JoinRequest, JoinRequestRepository]):
    """Сервис для работы с заявками в закрытый канал"""

    def __init__(self, session: AsyncSession):
        super().__init__(JoinRequest, session, JoinRequestRepository)


    async def send_jr(self, user: User, channel: Container):
        """Создается при попытке подписки на приватный канал"""

        jr = await self.repository.get_one_by(user_id=user.id, container_id=channel.id)

        if jr:
            await self.delete_item(jr)
        await self.create_item(user_id=user.id, container_id=channel.id)



