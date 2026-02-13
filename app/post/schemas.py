from pydantic import Field

from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from reaction.schemas import ReactionsCount
from container.schemas import ContainerShow


class PostAllows(BaseSchema):
    allow_comments: bool | None = None
    allow_reactions:  bool | None = None


class PostBase(BaseSchema):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(max_length=5000)


from user.schemas import ShortUserInfo


class PostShow(PostBase, IdMixinSchema, TimeMixinSchema):
    author: ShortUserInfo
    slug: str
    container: ContainerShow | None
    allow_comments: bool
    allow_reactions: bool


class PostSlug(BaseSchema):
    slug: str

class TopPostShow(BaseSchema):
    post: PostShow
    count: int


class FullPostShow(BaseSchema):
    post: PostShow
    reactions: ReactionsCount



class PostCreate(PostBase):
    container_id: int | None = None



class PostUpdate(BaseSchema):
    content: str = Field(max_length=5000)




