from base.schemas import BaseSchema

class BaseChannelCreate(BaseSchema):
    title: str | None = None
    description: str | None = None


class ChannelCreate(BaseChannelCreate):
    slug: str | None = None
    is_private: bool = False


class CreatePublic(BaseChannelCreate):
    slug: str


class CreatePrivate(BaseChannelCreate):
    slug: None = None

