from base.schemas import BaseSchema
from typing import Literal


class ListOfSubscribes(BaseSchema):
    user_subs: list[int]
    topic_subs: list[int]


subscribe_type = Literal["user", "topic"]






