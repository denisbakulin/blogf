from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from schemas.user import UserUsername

class CommentBase(BaseSchema):
    content: str


class CommentCreate(CommentBase):
    parent_id: int | None = None


class CommentShow(CommentCreate, IdMixinSchema, TimeMixinSchema):
    pass

class CommentFullShow(CommentShow):
    author_username: str
    post_slug: str

class CommentAuthorShow(CommentShow):
    author: UserUsername


class CommentUpdate(CommentBase):
    pass





