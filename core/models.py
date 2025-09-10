from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import inspect
from typing import Optional, Callable
from pydantic import BaseModel, Field


class ColumnProps(BaseModel):
    name: str
    type: str
    nullable: bool = Field(default=False)
    primary_key: bool = Field(default=False)
    unique: bool = Field(default=False)
    foreign_key: Optional[str] = Field(default=None)



class BaseORM(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    depends: Optional[list[tuple[str, Callable]]] = None

    def __init__(self, **kwargs):
        if self.depends is not None:
            for dep_name, dep in self.depends:
                setattr(self, dep_name, dep())

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        super().__init__()

    @classmethod
    def table_info(cls) -> list[ColumnProps]:
        inspector = inspect(cls)
        columns_info = []

        for column in inspector.mapper.columns:

            column_type = str(column.type)

            foreign_key_info = None

            if column.foreign_keys:
                fk = list(column.foreign_keys)[0]
                foreign_key_info = f"{fk.column.table.name}.{fk.column.name}"

            columns_info.append(
                ColumnProps(
                    name=column.name,
                    type=column_type,
                    nullable=bool(column.nullable),
                    primary_key=bool(column.primary_key),
                    unique=bool(column.unique),
                    foreign_key=foreign_key_info
                )
            )

        print(columns_info)
        return columns_info
    

