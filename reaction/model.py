from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.model import BaseORM, TimeMixin


class Reaction(BaseORM, TimeMixin):
    __tablename__ = "user_reaction_post"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), primary_key=True)
    reaction: Mapped[str] = mapped_column(nullable=False)





