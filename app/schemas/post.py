from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from pydantic import Field
from schemas.container import ContainerShow

from schemas.user import UserUsername


class PostBase(BaseSchema):
    title: str = Field(min_length=3, max_length=100)
    content: str = Field(min_length=10, max_length=5000)


class PostSlug(BaseSchema):
    slug: str


class PostShow(PostBase, IdMixinSchema, TimeMixinSchema):
    slug: str
    allow_comments: bool
    allow_reactions: bool

class PostAuthorShow(PostShow):
    author: UserUsername


class PostFullShow(PostShow):
    author: UserUsername
    container: ContainerShow


class TopPostShow(BaseSchema):
    post: PostShow
    like_count: int



class PostCreate(PostBase):
    allow_comments: bool | None = None
    allow_reactions: bool | None = None


class PostUpdate(BaseSchema):
    content: str = Field(max_length=5000)




