from enum import StrEnum

from base.model import BaseORM, IdMixin, TimeMixin, OwnedByUserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class ReactionType(StrEnum):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"


class Reaction(BaseORM, TimeMixin, IdMixin, OwnedByUserMixin):
    __tablename__ = "user_reactions"

    post_id: Mapped[int | None] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE")
    )

    type: Mapped[ReactionType]





