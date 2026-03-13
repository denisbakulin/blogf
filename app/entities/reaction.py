from enum import StrEnum

from base.model import BaseORM, IdMixin, TimeMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class ReactionType(StrEnum):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"


class Reaction(BaseORM, TimeMixin, IdMixin):
    __tablename__ = "user_reactions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int | None] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE")
    )
    container_id: Mapped[int | None] = mapped_column(
        ForeignKey("containers.id", ondelete="CASCADE")
    )

    type: Mapped[ReactionType]





