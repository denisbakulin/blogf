from pydantic import Field, BaseModel

from core.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema


class PostAllows(BaseSchema):
    allow_comments: bool = Field(default=True)
    allow_reactions: bool = Field(default=True)

class PostBase(PostAllows):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(max_length=5000)
    public: bool = Field(default=True)


from user.schemas import PostUserShow

class PostShow(PostBase, IdMixinSchema, TimeMixinSchema):
    author: PostUserShow
    slug: str


class TopPostShow(BaseSchema):
    post: PostShow
    count: int

class PostReactions(BaseModel):
    like: int = 0
    love: int = 0
    dislike: int = 0


class FullPostShow(BaseSchema):
    post: PostShow
    reactions: PostReactions



class PostCreate(PostBase):
    ...


class PostUpdate(BaseSchema):
    content: str = Field(max_length=5000)
    public: bool




