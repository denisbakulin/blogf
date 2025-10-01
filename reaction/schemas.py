from datetime import datetime

from core.schemas import BaseSchema


class ReactionShow(BaseSchema):
    user_id: int
    post_id: int
    reaction: str
    created_at: datetime
