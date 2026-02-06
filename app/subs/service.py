from sqlalchemy.ext.asyncio import AsyncSession

from base.exceptions import EntityBadRequestError
from base.service import BaseService

from helpers.search import Pagination
from subs.schemas import subscribe_type
from subs.model import Subscribe
from subs.repository import SubscribeRepository
from user.model import User
from topic.release.service import TopicService
from user.service import UserService

from post.service import PostService
class SubscribeService(BaseService[Subscribe, SubscribeRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Subscribe, session, SubscribeRepository)
        self.user_service = UserService(session=session)
        self.topic_service = TopicService(session=session)
        self.post_service = PostService(session=session)

    async def process_subscribe(self, user: User, sub_type: subscribe_type, entity_id: int):
        if sub_type == "user":
            creator = await self.user_service.get_user_by_id(entity_id)
            if creator.id == user.id:
                raise EntityBadRequestError("Подписка", "Нельзя подписаться на самого себя")

            sub = await self.repository.get_one_by(
                user_id=user.id, creator_id=creator.id
            )
            create_dict = {"creator_id": entity_id}
        else:
            topic = await self.topic_service.get_item_by_id(entity_id)

            sub = await self.repository.get_one_by(
                user_id=user.id, topic_id=topic.id
            )
            create_dict = {"topic_id": entity_id}

        if sub:
            await self.delete_item(sub)
        else:
            await self.create_item(user_id=user.id, **create_dict)

    async def _get_creator_ids(self, user_id: int):
        user_subs = await self.repository.get_any_by(user_id=user_id, topic_id=None, lines=["creator_id"]) or []
        return list(i[0] for i in user_subs)

    async def _get_topic_ids(self, user_id: int):
        user_subs = await self.repository.get_any_by(user_id=user_id, creator_id=None,lines=["topic_id"]) or []
        return list(i[0] for i in user_subs)

    async def get_subs(self, user: User):
        user_subs = await self._get_creator_ids(user.id)
        topic_subs = await self._get_topic_ids(user.id)
        return {
            "user_subs": user_subs,
            "topic_subs": topic_subs
        }

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









