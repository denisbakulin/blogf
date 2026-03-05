from functools import partial
from base.service import BaseService
from helpers.search import Pagination

from entities.post import Post
from entities.reaction import Reaction, ReactionType
from repositories.reaction import ReactionRepository
from schemas.reaction import ReactionsCount
from sqlalchemy.ext.asyncio import AsyncSession



class ReactionService(BaseService[Reaction, ReactionRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Reaction, session, ReactionRepository)


    async def process_post_reaction(
            self,
            user_id: int,
            post_id: int,
            reaction: ReactionType,
    ):
        _reaction = await self.repository.get_one_by(user_id=user_id, post_id=post_id)

        if _reaction:
            await self.delete_item_by_id(_reaction.id)

        await self.create_item(user_id=user_id, post_id=post_id, type=reaction)

    async def process_container_reaction(
            self, user_id: int,
            container_id: int,
            reaction: ReactionType
    ):
        _reaction = await self.repository.get_one_by(user_id=user_id, container_id=container_id)

        if _reaction:
            await self.delete_item_by_id(_reaction.id)

        await self.create_item(user_id=user_id, container_id=container_id, type=reaction)



    # async def get_post_reactions(
    #         self, post_id: int,
    #         reaction_type: ReactionType,
    #         pagination: Pagination
    # ) -> list[Reaction]:
    #     default_get = partial(self.repository.get_any_by, post_id=post_id, **pagination.dict())
    #
    #     return await self._get_reactions(default_get, reaction_type)
    #
    # async def get_container_reactions(
    #         self, container_id: int,
    #         reaction_type: ReactionType,
    #         pagination: Pagination
    # ) -> list[Reaction]:
    #     default_get = partial(self.repository.get_any_by, container_id=container_id, **pagination.dict())
    #
    #     return await self._get_reactions(default_get, reaction_type)


    # async def get_user_reactions(self, user_id: int, reaction_type: ReactionType, pagination: Pagination) -> list[Reaction]:
    #     default_get = partial(self.repository.get_any_by, user_id=user_id, **pagination.dict())
    #
    #     return await self._get_reactions(default_get, reaction_type)
    #
    #
    # async def get_post_reaction_count(self, post: Post) -> ReactionsCount:
    #     reactions = await self.repository.get_post_reaction_count(post=post)
    #
    #     return ReactionsCount(**reactions)
    #
    # async def _get_reactions(self, default, reaction):
    #     if reaction == "all":
    #         return await default()
    #     return await default(reaction=reaction)








