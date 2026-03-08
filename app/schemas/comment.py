from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema


class CommentBase(BaseSchema):
    content: str


class CommentCreate(CommentBase):
    parent_id: int | None = None


class CommentShow(CommentCreate, IdMixinSchema, TimeMixinSchema):
    author_username: str
    post_slug: str


class CommentUpdate(CommentBase):
    ...





