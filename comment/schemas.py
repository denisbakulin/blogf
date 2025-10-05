from typing import Optional

from core.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema


class CommentBase(BaseSchema):
    content: str

class CommentCreate(CommentBase):
    parent_id: Optional[int] = None


class CommentShow(CommentCreate, IdMixinSchema, TimeMixinSchema):
    user_id: int


class CommentUpdate(CommentBase):
    ...





