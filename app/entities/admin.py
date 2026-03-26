from base.model import BaseORM, IdMixin, TimeMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Admin(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "admins"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    container_id: Mapped[int | None] = mapped_column(ForeignKey("containers.id"))






