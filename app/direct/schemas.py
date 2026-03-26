from base.schemas import BaseSchema, IdMixinSchema, CreatedAtMixinSchema
from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: str


class DirectMessageShow(MessageCreate, CreatedAtMixinSchema, IdMixinSchema):
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

