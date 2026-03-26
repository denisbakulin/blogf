from base.schemas import (
    BaseSchema,
    IdMixinSchema,
    CreatedAtMixinSchema,
    UpdatedAtMixinSchema
)

from schemas.user import UserUsername

class CommentBase(BaseSchema):
    content: str


class CommentCreate(CommentBase):
    parent_id: int | None = None


class CommentShow(CommentCreate, IdMixinSchema, CreatedAtMixinSchema, UpdatedAtMixinSchema):
    pass

class CommentFullShow(CommentShow):
    author: UserUsername
    post_slug: str


class CommentAuthorShow(CommentShow):
    author: UserUsername


class CommentUpdate(CommentBase):
    pass





