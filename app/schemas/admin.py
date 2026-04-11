from base.schemas import BaseSchema


class AdminCreate(BaseSchema):
    user_id: int
    container_id: int

