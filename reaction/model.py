from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model import BaseORM, TimeMixin


class Reaction(BaseORM, TimeMixin):
    __tablename__ = "user_reaction_post"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)


    post: Mapped["Post"] = relationship("Post")
    user: Mapped["Post"] = relationship("User")


    reaction: Mapped[str] = mapped_column(nullable=False)





