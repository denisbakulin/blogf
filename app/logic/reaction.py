from abac.reaction.policy import ReactionPolicy
from entities import ReactionType, User
from helpers.search import Pagination
from services.container import AsyncSession, ContainerService
from services.post import PostService
from services.reaction import ReactionService


__all__ = (
    "GetPostReactionsUseCase",
    "ProcessPostReactionUseCase"
)


class BaseReactionUseCase:
    def __init__(
            self,
            session: AsyncSession
    ):
        self.post_service = PostService(session)
        self.container_service = ContainerService(session)
        self.reaction_service = ReactionService(session)
        self.session = session
        self.policy = ReactionPolicy(self.session)


class GetPostReactionsUseCase(BaseReactionUseCase):
    async def execute(self, user: User, post_slug: str, pagination: Pagination):
        post = await self.post_service.get_by_or_raise(slug=post_slug)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_read(user=user, container=container)

        return await self.reaction_service.get_post_reactions(
            post_id=post.id, pagination=pagination
        )


class ProcessPostReactionUseCase(BaseReactionUseCase):

    async def execute(self, user: User, post_slug: str, reaction: ReactionType | None = None):
        post = await self.post_service.get_by_or_raise(slug=post_slug)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_create(user=user, container=container)

        await self.reaction_service.process_post_reaction(
            user_id=user.id, reaction=reaction, post_id=post.id
        )











