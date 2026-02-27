from base.model import BaseORM, IdMixin, TimeMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Subscribe(BaseORM, TimeMixin, IdMixin):
    __tablename__ = "user_subscribes"

    container_id: Mapped[int | None] = mapped_column(ForeignKey("containers.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship("User", lazy="selectin", foreign_keys=[user_id])
    container: Mapped["Container"] = relationship("Container", lazy="selectin", foreign_keys=[container_id])


