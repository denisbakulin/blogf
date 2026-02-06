from typing import Literal

default_reactions = ("like", "dislike")

ReactionsGetParams = Literal[*default_reactions, "all"]
ReactionsSetParams = Literal[*default_reactions]