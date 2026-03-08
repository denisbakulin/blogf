from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base.model import BaseORM, IdMixin


class AllowAction(StrEnum):
    CREATE = "create"
    EDIT = "edit"
    DELETE = "delete"
    READ = "read"

class AllowEntity(StrEnum):
    USER = "user"
    CONTAINER = "container"
    POST = "post"
    COMMENT = "comment"
    REACTION = "reaction"

class Allow(BaseORM, IdMixin):
    __tablename__ = "user_allows"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action: Mapped[AllowAction]
    entity: Mapped[AllowEntity]
    against: Mapped[bool] = mapped_column(default=False)

    context: Mapped[AllowEntity | None]
    context_id: Mapped[int | None]

    user: Mapped["User"] = relationship("User", lazy="selectin")
