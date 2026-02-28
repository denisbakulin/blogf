from base.exceptions import EntityBadRequestError
from base.service import BaseService
from models.container import ContainerType as ct
from models.subscribe import Subscribe
from repositories.subscribe import SubscribeRepository
from schemas.container import ContainerShow
from schemas.subscribe import ContainerSubs, ListOfSubscribes
from services.container import ContainerService
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserUsername
from models.user import  User


class SubscribeService(BaseService[Subscribe, SubscribeRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Subscribe, session, SubscribeRepository)
        self.container_service = ContainerService(session=session)


    async def create_subscribe(
            self, user: User,
            container_id: int | None = None,
            creator_id: int | None = None
    ):
        if container_id and creator_id or not (container_id or creator_id):
            raise EntityBadRequestError(entity="Подписка")

        subscribe = await self.repository.get_one_by(
            user_id=user.id, container_id=container_id, creator_id=creator_id
        )

        if subscribe:
            await self.delete_item(subscribe)
        else:
            await self.create_item(
                user_id=user.id,
                container_id=container_id,
                creator_id=creator_id
            )


    async def get_subs(self, user: User) -> ListOfSubscribes:
        subs = await self.repository.get_any_by(user_id=user.id)
        creators = [UserUsername.from_orm(i.creator) for i in subs if i.creator_id is not None]
        topics = [ContainerShow.from_orm(i.container) for i in subs if i.container.type == ct.topic]
        private = [ContainerShow.from_orm(i.container) for i in subs if i.container.type == ct.private_channel]
        public = [ContainerShow.from_orm(i.container) for i in subs if i.container.type == ct.public_channel]

        return ListOfSubscribes(
            creator_subs=creators,
            container_subs=ContainerSubs(
                topics=topics,
                private_channels=private,
                public_channels=public
            )
        )

    async def is_subscriber(self, user_id: int, container_id: int):
        exists = await self.repository.exists(user_id=user_id, container_id=container_id)
        return exists







