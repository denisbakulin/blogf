from base.schemas import BaseSchema


class ChannelCreate(BaseSchema):
    slug: str
    title: str
    description: str | None = None
    is_private: bool = False

