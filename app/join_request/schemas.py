from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from user.schemas import ShortUserInfo


class JRShow(BaseSchema, TimeMixinSchema, IdMixinSchema):
    user: ShortUserInfo




