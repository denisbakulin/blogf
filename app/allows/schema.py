from allows.model import AllowAction, DBEntity
from base.schemas import BaseSchema


class AllowBase(BaseSchema):
    action: AllowAction
    entity: DBEntity
    against: bool

    context: DBEntity | None
    context_id: int | None


class AllowShow(AllowBase):
    user_id: int
