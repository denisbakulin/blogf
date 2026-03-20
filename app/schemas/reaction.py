from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from entities import ReactionType
from pydantic import BaseModel
from schemas.post import PostSlug
from schemas.user import UserUsername


class ReactionsCount(BaseModel):
    like: int = 0
    dislike: int = 0


class Slug(BaseSchema):
    slug: str


class ReactionShow(BaseSchema, TimeMixinSchema, IdMixinSchema):
    type: ReactionType

class UserReactionShow(ReactionShow):
    post: PostSlug



class BaseReactionShow(BaseSchema, TimeMixinSchema):
    reaction: str
    user: UserUsername

class PostReactionShow(BaseReactionShow, TimeMixinSchema):
    post: PostSlug

class TopicReactionShow(BaseReactionShow, TimeMixinSchema):
    container: Slug



