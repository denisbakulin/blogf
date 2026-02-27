from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from schemas.user import ShortUserInfo


class JRShow(BaseSchema, TimeMixinSchema, IdMixinSchema):
    user: ShortUserInfo




