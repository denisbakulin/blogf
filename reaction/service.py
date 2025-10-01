from functools import partial

from sqlalchemy.ext.asyncio import AsyncSession

from core.service import BaseService
from helpers.search import Pagination
from post.dependencies import PostService
from post.model import Post
from reaction.model import Reaction
from reaction.repository import ReactionRepository
from user.model import User


class ReactionService(BaseService):

    def __init__(self, session: AsyncSession):
        super().__init__(Reaction, session, ReactionRepository)

    async def add_reaction(self, user: User, post: Post, reaction_type: str):
        reaction = await self.repository.get_one_by(user_id=user.id, post_id=post.id)

        if reaction:
            await self.delete_item(reaction)


        return await self.create_item(user_id=user.id, post_id=post.id, reaction=reaction_type)


    async def get_post_reactions(self, post: Post, reaction_type: str, pagination: Pagination) -> list[Reaction]:
        default_get = partial(self.repository.get_any_by, post_id=post.id, **pagination.get())

        return await self._get_reactions(default_get, reaction_type)


    async def get_user_reactions(self, user: User, reaction_type: str, pagination: Pagination) -> list[Reaction]:
        default_get = partial(self.repository.get_any_by, user_id=user.id, **pagination.get())

        return await self._get_reactions(default_get, reaction_type)


    async def _get_reactions(self, default, reaction):
        if reaction == "all":
            return await default()
        return await default(reaction=reaction)








