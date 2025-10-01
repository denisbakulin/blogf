from datetime import datetime
from typing import Optional

from core.schemas import BaseSchema


class CommentBase(BaseSchema):
    content: str

class CommentCreate(CommentBase):
    parent_id: Optional[int] = None


class CommentShow(CommentCreate):
    id: int
    user_id: int
    created_at: datetime

class CommentUpdate(CommentBase):
    ...





