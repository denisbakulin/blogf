from pydantic import BaseModel

from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema


class MessageCreate(BaseModel):
    content: str


class DirectMessageShow(MessageCreate, TimeMixinSchema, IdMixinSchema):
    recipient_id: int
    sender_id: int



class BaseDirectEvent(BaseModel):
    type: str
    data: dict

class ClientDirectEvent(BaseDirectEvent):
    initiator_id: int



class DirectUserSettingsSchema(BaseSchema):
    chat_name: str | None = None
    enable_notifications: bool
    banned: bool


class DirectChatShow(BaseModel):
    settings: DirectUserSettingsSchema
    user: UserShow

