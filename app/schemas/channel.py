from base.schemas import BaseSchema, IdMixinSchema

class ChannelID(BaseSchema, IdMixinSchema):
    pass

class BaseChannelCreate(BaseSchema):
    title: str | None = None
    description: str | None = None


class CreatePublic(BaseChannelCreate):
    slug: str


class CreatePrivate(BaseChannelCreate):
    pass

