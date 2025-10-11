from core.schemas import BaseSchema
from user.schemas import UserShow

class BaseTopic(BaseSchema):
    title: str
    slug: str | None = None
    description: str | None = None


class CreateTopic(BaseTopic):
    slug: str


class UserCommentsCountOfTopicShow(BaseSchema):
    count: int
    topic: BaseTopic

class TopicOfferShow(BaseTopic):
    status: str
    author: UserShow



from typing import Literal
class AddTopicByOffer(BaseTopic):
    status: Literal["approve", "reject"]

