from sqlalchemy.ext.asyncio import AsyncSession

from base.exceptions import EntityBadRequestError
from base.service import BaseService

from helpers.search import Pagination
from sub.schemas import subscribe_type
from sub.model import Subscribe
from sub.repository import SubscribeRepository
from user.model import User

from container.model import Container, ContainerType as ct
from container.service import ContainerService
from sub.schemas import ListOfSubscribes, ContainerSubs
from user.schemas import ShortUserInfo
from container.schemas import ContainerShow

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
        creators = [ShortUserInfo.from_orm(i.creator) for i in subs if i.creator_id is not None]
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

    async def get_content(
            self, user: User,
            sub_type: subscribe_type | None,
            pagination: Pagination
    ):

        if sub_type == "user":
            user_ids = await self._get_creator_ids(user.id)
            posts = await self.repository.get_creators_posts(
                ids=user_ids, **pagination.dict()
            )
        elif sub_type == "topic":
            topic_ids = await self._get_topic_ids(user.id)
            posts = await self.repository.get_topics_posts(
                ids=topic_ids, **pagination.dict()
            )

        else:
            user_ids = await self._get_creator_ids(user.id)
            topic_ids = await self._get_topic_ids(user.id)
            posts = await self.repository.get_mixed_posts(
                uids=user_ids, tids=topic_ids,  **pagination.dict()
            )

        return list(posts)









