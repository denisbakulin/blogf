from base.model import BaseORM, IdMixin, TimeMixin, OwnedByUserMixin, DBEntity
from sqlalchemy.orm import Mapped, mapped_column


class Report(BaseORM, IdMixin, TimeMixin, OwnedByUserMixin):
    __tablename__ = "reports"

    reason: Mapped[str | None] = mapped_column(default=None)
    entity_id: Mapped[int]
    entity_type: Mapped[DBEntity]



