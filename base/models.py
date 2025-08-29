from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import ConfigDict

class BaseORM(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    
