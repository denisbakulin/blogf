from pydantic import BaseModel
from core.schemas import TimeMixinSchema, IdMixinSchema


class MessageCreate(BaseModel):
    content: str


class DirectMessageShow(MessageCreate, TimeMixinSchema, IdMixinSchema):
    recipient_id: int
    sender_id: int

from user.schemas import UserShow

class DirectChatShow(BaseModel):
    chat_name: str
    user: UserShow


class BaseDirectEvent(BaseModel):
    type: str
    data: dict

class ClientDirectEvent(BaseDirectEvent):
    initiator_id: int



class DirectUserSettingsSchema(BaseModel):
    chat_name: str | None = None
    enable_notifications: bool | None = None





