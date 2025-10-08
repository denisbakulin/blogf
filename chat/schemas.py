from datetime import datetime
from pydantic import BaseModel
from core.schemas import TimeMixinSchema, IdMixinSchema


class MessageCreate(BaseModel):
    content: str

class BaseMessageShow(MessageCreate, TimeMixinSchema, IdMixinSchema):
    sender_id: int

class DirectMessageShow(BaseMessageShow):
    recipient_id: int

class GeneralMessageShow(BaseMessageShow):
    chat_id: int


class DirectChatShow(BaseModel, TimeMixinSchema):
    first_user_id: int
    second_user_id: int
    banned_user_id: int | None


class BaseDirectEvent(BaseModel):
    type: str
    data: dict

class ClientDirectEvent(BaseDirectEvent):
    initiator_id: int







