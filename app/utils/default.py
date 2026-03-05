from dataclasses import dataclass, fields
from typing import Any, Type, TypeVar

D = TypeVar('D')


def to_dto(model: Any, dataclass_type: Type[D]) -> D:
    """
    Конвертирует любую модель в dataclass
    """

    # Получаем поля dataclass
    dataclass_fields = {f.name for f in fields(dataclass_type)}

    # Фильтруем атрибуты модели, которые есть в dataclass
    valid_attrs = {
        name: getattr(model, name)
        for name in dataclass_fields
        if hasattr(model, name)
    }

    return dataclass_type(**valid_attrs)