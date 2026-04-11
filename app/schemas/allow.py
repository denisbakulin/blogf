from base.schemas import BaseSchema
from base.model import DBEntity
from entities import AllowAction


class AllowCreate(BaseSchema):
    container_id: int
    against: bool
    entity: DBEntity
    action: AllowAction
    user_id: int


