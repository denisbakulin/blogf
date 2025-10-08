from core.model import BaseORM, IdMixin
from sqlalchemy.orm import Mapped


class UsedToken(BaseORM, IdMixin):
    __tablename__ = "used_tokens"

    type: Mapped[str]
    token: Mapped[str]


