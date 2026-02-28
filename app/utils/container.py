from typing import Literal
from helpers.search import search_param_fabric


ContainerSearchParams = search_param_fabric(Literal["slug", "title"])