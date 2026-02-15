from base.schemas import BaseSchema
from allows.model import AllowAction, AllowEntity


class AllowBase(BaseSchema):
    action: AllowAction
    entity: AllowEntity
    against: bool

    context: AllowEntity | None
    context_id: int | None


class AllowShow(AllowBase):
    user_id: int
