from base.service import BaseService
from entities import Reaction, ReactionType, User, Post

from helpers.search import Pagination
from repositories.reaction import ReactionRepository
from sqlalchemy.ext.asyncio import AsyncSession


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
    ) -> list[tuple[Reaction, User]]:

        return await self.repository.get_post_reactions(
            post_id=post_id, type_=reaction_type, **pagination.dict()
        )


    async def get_user_reactions(
            self, user_id: int,
            pagination: Pagination,
            reaction_type: ReactionType | None = None,
        ) -> list[tuple[Reaction, Post]]:

        return await self.repository.get_user_reactions(
            user_id=user_id, type_=reaction_type, **pagination.dict()
        )







