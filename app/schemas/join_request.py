from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from schemas.user import UserUsername

class JRShow(BaseSchema, TimeMixinSchema, IdMixinSchema):
    pass

class JRSUserShow(JRShow):
    user: UserUsername




