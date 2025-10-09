from subs.repository import SubscribeRepository
from sqlalchemy.ext.asyncio import AsyncSession
from core.service import BaseService

from subs.model import Subscribe

from direct.ws import WebSocketManager
from user.model import User
from helpers.search import Pagination

from core.exceptions import EntityBadRequestError
class SubscribeService(BaseService[Subscribe, SubscribeRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Subscribe, session, SubscribeRepository)
        self.ws_manager = WebSocketManager()

    async def process_subscribe(self, subscriber: User, creator: User) -> Subscribe:
        if subscriber.id == creator.id:
            raise EntityBadRequestError("Подписка", "Нельзя подписаться на самого себя")

        subs = await self.repository.get_one_by(subscriber_id=subscriber.id, creator_id=creator.id)

        if subs:
            return await self.delete_item(subs)

        return await self.create_item(subscriber_id=subscriber.id, creator_id=creator.id)



    async def get_user_subscribes(self, user: User, pagination: Pagination) -> list[Subscribe]:
        return await self.repository.get_any_by(subscriber_id=user.id, **pagination.get())






