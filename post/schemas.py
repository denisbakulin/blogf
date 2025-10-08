from pydantic import Field, BaseModel

from core.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema


class PostBase(BaseSchema):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(max_length=5000)
    public: bool = Field(default=True)
    allow_comments: bool = Field(default=True)
    allow_reactions: bool = Field(default=True)


class PostShow(PostBase, IdMixinSchema, TimeMixinSchema):
    author_id: int
    slug: str

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




