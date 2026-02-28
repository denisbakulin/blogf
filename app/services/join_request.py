from base.service import BaseService
from models.join_request import JoinRequest
from repositories.join_request import JoinRequestRepository
from sqlalchemy.ext.asyncio import AsyncSession
from DTO.join_request import JoinRequestDTO


class JoinRequestService(BaseService[JoinRequest, JoinRequestRepository, JoinRequestDTO]):
    """Сервис для работы с заявками в закрытый канал"""

    def __init__(self, session: AsyncSession):
        super().__init__(JoinRequest, session, JoinRequestRepository)


    async def send_jr(self, user_id: int, channel_id: int):
        """Создается при попытке подписки на приватный канал"""

        jr = await self.repository.get_one_by(user_id=user_id, container_id=channel_id)

        if jr:
            await self.delete_item_by_id(jr.id)
        await self.create_item(user_id=user_id, container_id=channel_id)





