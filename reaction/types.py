from typing import Literal


default_reactions = ("love", "like", "dislike")


PostReactionsGetParams = UserReactions = Literal[*default_reactions, "all"]
PostReactionsSetParams = Literal[*default_reactions]