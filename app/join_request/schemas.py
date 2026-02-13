from base.schemas import BaseSchema, TimeMixinSchema, IdMixinSchema
from user.schemas import ShortUserInfo

class JRShow(BaseSchema, TimeMixinSchema, IdMixinSchema):
    user: ShortUserInfo




