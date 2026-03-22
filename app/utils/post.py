from re import sub
from typing import Literal

from helpers.search import search_param_fabric
from unidecode import unidecode


def generate_slug(title: str) -> str:
    """Приводит строку к виду 'abc-de-f-g' путем
    транслитерации с русского(англ.) на английский
    и отброса специальных символов, убирая их или заменяя на '-'.

    Пример:
    'Привет! каК дела?,.' -> 'privet-kak-dela'"""

    result = sub(
        r"[^a-z0-9]+",
        "-",
        unidecode(title.lower())
    )

    return result.strip("-")

def add_metadata_to_slug(slug: str, **metadata) -> str:
    return slug + "".join(f"-{key}!{value}" for key, value in metadata.items())



PostSearchParams = search_param_fabric(Literal["slug", "id", "title"])

