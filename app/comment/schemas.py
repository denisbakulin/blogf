from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from post.schemas import PostSlug
from user.schemas import ShortUserInfo


class CommentBase(BaseSchema):
    content: str


class CommentCreate(CommentBase):
    parent_id: int | None = None


class CommentShow(CommentCreate, IdMixinSchema, TimeMixinSchema):
    author: ShortUserInfo
    post: PostSlug


class CommentUpdate(CommentBase):
    ...





