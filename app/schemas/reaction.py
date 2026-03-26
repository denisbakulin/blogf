from base.schemas import BaseSchema, IdMixinSchema, CreatedAtMixinSchema
from entities import ReactionType
from pydantic import BaseModel
from schemas.post import PostSlug
from schemas.user import UserUsername


class ReactionsCount(BaseModel):
    like: int = 0
    dislike: int = 0


class Slug(BaseSchema):
    slug: str


class ReactionShow(BaseSchema, CreatedAtMixinSchema):
    type: ReactionType



class ReactionAuthorShow(ReactionShow):
    author: UserUsername


class ReactionPostShow(ReactionShow):
    post: PostSlug


class TopicReactionShow(ReactionAuthorShow, CreatedAtMixinSchema):
    container: Slug



