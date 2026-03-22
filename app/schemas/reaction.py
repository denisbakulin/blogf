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


class ReactionShow(BaseSchema, TimeMixinSchema):
    type: ReactionType



class ReactionAuthorShow(ReactionShow):
    author: UserUsername


class ReactionPostShow(ReactionShow):
    post: PostSlug


class TopicReactionShow(ReactionAuthorShow, TimeMixinSchema):
    container: Slug



