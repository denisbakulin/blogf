from base.schemas import IdMixinSchema
from models.topic_offer import TopicOfferStatus
from schemas.topic import TopicBase


class CreateTopicOffer(TopicBase):
    ...


class TopicOfferShow(CreateTopicOffer, IdMixinSchema):
    status: TopicOfferStatus
    author_username: str
    process_user_username: str | None


