from base.service import BaseService
from entities.subscribe import Subscribe
from helpers.search import Pagination
from repositories.subscribe import SubscribeRepository
from sqlalchemy.ext.asyncio import AsyncSession


class SubscribeService(BaseService[Subscribe, SubscribeRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Subscribe, session, SubscribeRepository)


    async def create_subscribe(
            self, user_id: int,
            container_id: int,
    ):
        subscribe = await self.repository.get_one_by(
            user_id=user_id, container_id=container_id
        )

        if subscribe:
            await self.delete_item_by_id(subscribe.id)
        else:
            await self.create_item(
                user_id=user_id,
                container_id=container_id,
            )


    async def get_subs(self, user_id: int, pagination: Pagination):
       return await self.repository.get_user_subs(user_id, **pagination.dict())



    async def is_subscriber(self, user_id: int, container_id: int):
        exists = await self.repository.exists(user_id=user_id, container_id=container_id)
        return exists

    async def get_content(self, user_id: int, pagination: Pagination):

        return await self.repository.get_user_content(user_id=user_id, **pagination.dict())






