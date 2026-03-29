from abac.container.policy import TopicPolicy
from base.exceptions import EntityBadRequestError

from entities import User, TopicOfferStatus
from services.topic import TopicService
from services.container import AsyncSession
from schemas.topic import CreateTopic, AddTopicByOffer

__all__ = (
    "CreateTopicUseCase",
    "CreateTopicFromOfferUseCase"
)

from services.topic_offer import TopicOfferService
from utils.post import generate_slug


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


class CreateTopicFromOfferUseCase(BaseTopicUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offer_service = TopicOfferService(self.session)

    async def execute(
        self,
        user: User,
        offer_id: int,
        process: AddTopicByOffer,
    ):
        topic_offer = await self.offer_service.get_topic_offer_by_id(offer_id)

        await self.policy.ensure_create(self.session, user_id=user.id)


        if topic_offer.status != TopicOfferStatus.PENDING:
            raise EntityBadRequestError(
                "offer-Тема", f"Предложенная тема уже имеет статус {topic_offer.status}"
            )

        await self.offer_service.update_item(
            topic_offer.id,
            status=process.status,
            process_user_id=user.id
        )

        if process.status == TopicOfferStatus.APPROVE:
            slug = generate_slug(process.slug)
            title = process.title or topic_offer.title
            description = process.description or topic_offer.description

            topic = CreateTopic(
                title=title,
                description=description,
                slug=slug
            )

            release_topic = await self.topic_service.create_topic(
                topic=topic, author_id=topic_offer.author_id
            )

            await self.offer_service.update_item(
                topic_offer.id,
                release_topic_id=release_topic.id
            )

        return topic_offer














