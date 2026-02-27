from base.model import BaseORM, IdMixin, TimeMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Reaction(BaseORM, TimeMixin, IdMixin):
    __tablename__ = "user_reactions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int | None] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE")
    )
    container_id: Mapped[int | None] = mapped_column(
        ForeignKey("containers.id", ondelete="CASCADE")
    )

    post: Mapped["Post"] = relationship("Post", lazy="selectin")
    container: Mapped["Container"] = relationship("Container", lazy="selectin")
    user: Mapped["User"] = relationship("User", lazy="selectin")



    reaction: Mapped[str] = mapped_column(nullable=False)





