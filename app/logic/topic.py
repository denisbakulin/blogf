from abac.container.policy import TopicPolicy

from entities import User, Container
from schemas.admin import AdminCreate
from schemas.container import ContainerUpdate, ContainerType
from services.topic import TopicService
from services.container import AsyncSession, ContainerService
from schemas.topic import CreateTopic

__all__ = (
    "CreateTopicUseCase"
)


class BaseTopicUseCase:
    def __init__(
        self, session: AsyncSession
    ):
        self.session = session
        self.policy = TopicPolicy
        self.topic_service = TopicService(session)





class CreateTopicUseCase(BaseTopicUseCase):

    async def execute(self, user: User, create: CreateTopic):
        await self.policy.ensure_create(self.session, user_id=user.id)

        return await self.topic_service.create_topic(
            topic=create, author_id=user.id
        )















