from base.schemas import BaseSchema, TimeMixinSchema
from pydantic import BaseModel
from user.schemas import ShortUserInfo


class ReactionsCount(BaseModel):
    like: int = 0
    love: int = 0
    dislike: int = 0


class Slug(BaseSchema):
    slug: str


class BaseReactionShow(BaseSchema, TimeMixinSchema):
    reaction: str
    user: ShortUserInfo

class PostReactionShow(BaseReactionShow, TimeMixinSchema):
    post: Slug

class TopicReactionShow(BaseReactionShow, TimeMixinSchema):
    container: Slug



