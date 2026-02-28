from base.service import BaseService
from entities.subscribe import Subscribe
from repositories.subscribe import SubscribeRepository
from sqlalchemy.ext.asyncio import AsyncSession



class SubscribeService(BaseService[Subscribe, SubscribeRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Subscribe, session, SubscribeRepository)


    async def create_subscribe(
            self, user_id: int,
            container_id: int | None = None,
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


    # async def get_subs(self, user: User) -> ListOfSubscribes:
    #     subs = await self.repository.get_any_by(user_id=user.id)
    #     walls = [UserUsername.from_orm(i.creator) for i in subs if i.creator_id == ContainerType.wall]
    #     topics = [ContainerShow.from_orm(i.container) for i in subs if i.container.type == ContainerType.topic]
    #     private = [ContainerShow.from_orm(i.container) for i in subs if i.container.type == ContainerType.private_channel]
    #     public = [ContainerShow.from_orm(i.container) for i in subs if i.container.type == ContainerType.public_channel]
    #
    #     return ListOfSubscribes(
    #         creator_subs=walls,
    #         container_subs=ContainerSubs(
    #             topics=topics,
    #             private_channels=private,
    #             public_channels=public
    #         )
    #     )

    async def is_subscriber(self, user_id: int, container_id: int):
        exists = await self.repository.exists(user_id=user_id, container_id=container_id)
        return exists







