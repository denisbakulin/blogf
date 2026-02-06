from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base.model import BaseORM, IdMixin, TimeMixin


class TopicOfferStatus(StrEnum):
    PENDING = "pending"
    APPROVE = "approve"
    REJECT = "reject"




class TopicOffer(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "topic_offers"

    title: Mapped[str]
    description: Mapped[str | None]
    status: Mapped[TopicOfferStatus] = mapped_column(default=TopicOfferStatus.PENDING)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(
        "User", lazy="selectin", foreign_keys=[author_id]
    )

    process_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    process_user: Mapped["User"] = relationship(
        "User", lazy="selectin", foreign_keys=[process_user_id]
    )

    release_topic_id: Mapped[int | None] = mapped_column(ForeignKey("containers.id"))

    release_topic: Mapped["Container"] = relationship(
        "Container", lazy="selectin"
    )










