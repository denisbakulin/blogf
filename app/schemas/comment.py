from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from schemas.post import PostSlug
from user import ShortUserInfo


class CommentBase(BaseSchema):
    content: str


class CommentCreate(CommentBase):
    parent_id: int | None = None


class CommentShow(CommentCreate, IdMixinSchema, TimeMixinSchema):
    author: ShortUserInfo
    post: PostSlug


class CommentUpdate(CommentBase):
    ...





