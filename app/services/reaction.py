from base.service import BaseService
from entities.reaction import Reaction, ReactionType
from repositories.reaction import ReactionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from functools import partial
from helpers.search import Pagination

class ReactionService(BaseService[Reaction, ReactionRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Reaction, session, ReactionRepository)

    async def process_post_reaction(
            self,
            user_id: int,
            post_id: int,
            reaction: ReactionType | None = None,
    ):
        ex_reaction = await self.repository.get_one_by(
            author_id=user_id, post_id=post_id
        )

        if ex_reaction:
            await self.delete_item_by_id(ex_reaction.id)

        if reaction is not None:
            await self.create_item(author_id=user_id, post_id=post_id, type=reaction)


    async def get_post_reactions(
            self, post_id: int,
            pagination: Pagination,
            reaction_type: ReactionType | None = None,
    ) -> list[Reaction]:

        default_get = partial(
            self.repository.get_any_by,
            post_id=post_id,
            **pagination.dict()
        )

        return await self._get_reactions(default_get, reaction_type)


    async def get_user_reactions(
            self, user_id: int,
            pagination: Pagination,
            reaction_type: ReactionType | None = None,
        ) -> list[Reaction]:

        default_get = partial(
            self.repository.get_any_by,
            author_id=user_id,
            **pagination.dict()
        )

        return await self._get_reactions(default_get, reaction_type)

    async def _get_reactions(self, default, reaction):
        if reaction is None:
            return await default()
        return await default(type=reaction)








