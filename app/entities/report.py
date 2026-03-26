from base.model import BaseORM, IdMixin, TimeMixin, OwnedByUserMixin, DBEntity
from sqlalchemy.orm import Mapped


class Report(BaseORM, IdMixin, TimeMixin, OwnedByUserMixin):
    __tablename__ = "reports"

    entity_id: Mapped[int]
    entity_type: Mapped[DBEntity]



