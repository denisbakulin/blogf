from core.schemas import BaseSchema
from datetime import datetime



class CommentBase(BaseSchema):
    content: str

class CommentCreate(CommentBase):
    parent_id: int
    post_id: int

class CommentUpdate(CommentBase):
    ...

class CommentShow(CommentBase):
    id: int
    user_id: int
    post_id: int
    parent_id: int
    created_at: datetime



