from typing import Literal

default_reactions = ("like", "dislike")

UserReactions = Literal[*default_reactions, "all", "love"]
PostReactionsGetParams = Literal[*default_reactions, "all"]
PostReactionsSetParams = Literal[*default_reactions, "love"]