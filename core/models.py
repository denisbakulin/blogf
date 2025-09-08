from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseORM(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    
