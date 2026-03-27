from base.model import BaseORM, IdMixin, TimeMixin, OwnedByUserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class InviteLink(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "invite_links"

    link: Mapped[str]
    container_id: Mapped[int] = mapped_column(ForeignKey("containers.id"))














