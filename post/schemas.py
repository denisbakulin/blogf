from core.schemas import BaseSchema
from pydantic import field_validator, Field
from typing import Optional
from post.utils import normalize_slug
from datetime import datetime


default_slug = "no-slug"


class PostBase(BaseSchema):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(max_length=5000)
    slug: Optional[str] = None

    @field_validator("slug", mode="before")
    def normalize_slug(cls, slug: Optional[str], info) -> str:
        if slug:
            return normalize_slug(slug, default_slug)
        return normalize_slug(info.data.get("title", ""), default_slug)


class PostCreate(PostBase):
    ...

class PostUpdate(PostBase):
    ...


class PostShow(PostCreate):
    id: int
    author_id: int
    created_at: datetime

