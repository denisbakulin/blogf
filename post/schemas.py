from core.schemas import BaseSchema
from pydantic import  Field

from datetime import datetime



class PostBase(BaseSchema):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(max_length=5000)


class PostShow(PostBase):
    id: int
    author_id: int
    created_at: datetime
    slug: str




class PostCreate(PostBase):
    ...


class PostUpdate(BaseSchema):
    content: str = Field(max_length=5000)



