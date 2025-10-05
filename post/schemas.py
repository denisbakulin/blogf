from datetime import datetime

from pydantic import Field, BaseModel

from core.schemas import BaseSchema


class PostBase(BaseSchema):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(max_length=5000)


class PostShow(PostBase):
    id: int
    author_id: int
    created_at: datetime
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



