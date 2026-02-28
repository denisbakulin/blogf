from base.model import BaseORM, IdMixin, TimeMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class JoinRequest(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "join_requests"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    container_id: Mapped[int] = mapped_column(ForeignKey("containers.id"))












