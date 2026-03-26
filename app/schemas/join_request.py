from base.schemas import BaseSchema, IdMixinSchema, CreatedAtMixinSchema
from schemas.user import UserUsername

class JRShow(BaseSchema, CreatedAtMixinSchema, IdMixinSchema):
    pass

class JRSUserShow(JRShow):
    user: UserUsername




