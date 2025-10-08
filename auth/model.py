from core.model import BaseORM, IdMixin
from sqlalchemy.orm import Mapped, mapped_column


class UsedToken(BaseORM, IdMixin):
    __tablename__ = "used_tokens"

    type: Mapped[str] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(nullable=False)


