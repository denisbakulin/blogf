from unidecode import unidecode
from re import sub


def generate_slug(title: str, index: int) -> str:
    """Приводит строку к виду 'abc-de-f-g' путем
    транслитерации с русского(англ.) на английский
    и отброса специальных символов, убирая их или заменяя на '-'.

    пример:
    'Привет! каК дела?,.' -> 'privet-kak-dela'"""

    result = sub(
        r"[^a-z0-9]+",
        "-",
        unidecode(f"{title} {index}").lower().strip("-")
    )

    return result


from helpers.search import search_param_fabric
from typing import Literal


PostSearchParams = search_param_fabric(Literal["slug", "id", "title"])

