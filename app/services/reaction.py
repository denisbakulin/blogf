
from functools import partial
from t.reaction import ReactionsSetParams

from base.exceptions import EntityBadRequestError
from base.service import BaseService
from helpers.search import Pagination
from models.container import Container
from models.post import Post
from models.reaction import Reaction
from repositories.reaction import ReactionRepository
from schemas.reaction import ReactionsCount
from sqlalchemy.ext.asyncio import AsyncSession
from user import User


class ReactionService(BaseService[Reaction, ReactionRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Reaction, session, ReactionRepository)


    async def process_post_reaction(
            self, user: User,
            reaction: ReactionsSetParams,
            post: Post
    ):
        if not post.allow_reactions:
            raise EntityBadRequestError(
                "Reaction",
                f"Под постом [{post.slug}] запрещено оставлять реакции"
            )
        _reaction = await self.repository.get_one_by(user_id=user.id, post_id=post.id)

        if _reaction:
            await self.delete_item(_reaction)

        await self.create_item(user_id=user.id, post_id=post.id, reaction=reaction)

    async def process_topic_reaction(
            self, user: User,
            container: Container,
            reaction: ReactionsSetParams
    ):
        _reaction = await self.repository.get_one_by(user_id=user.id, container_id=container.id)

        if _reaction:
            await self.delete_item(_reaction)

        await self.create_item(user_id=user.id, container_id=container.id, reaction=reaction)



    async def get_post_reactions(self, post: Post, reaction_type: str, pagination: Pagination) -> list[Reaction]:
        default_get = partial(self.repository.get_any_by, post_id=post.id, **pagination.dict())

        return await self._get_reactions(default_get, reaction_type)

    async def get_topic_reactions(self, topic: Container, reaction_type: str, pagination: Pagination) -> list[Reaction]:
        default_get = partial(self.repository.get_any_by, container_id=topic.id, **pagination.dict())

        return await self._get_reactions(default_get, reaction_type)


    async def get_user_reactions(self, user: User, reaction_type: str, pagination: Pagination) -> list[Reaction]:
        default_get = partial(self.repository.get_any_by, user_id=user.id, **pagination.dict())

        return await self._get_reactions(default_get, reaction_type)


    async def get_post_reaction_count(self, post: Post) -> ReactionsCount:
        reactions = await self.repository.get_post_reaction_count(post=post)

        return ReactionsCount(**reactions)

    async def _get_reactions(self, default, reaction):
        if reaction == "all":
            return await default()
        return await default(reaction=reaction)








