from base.exceptions import EntityBadRequestError, InsufficientPermissionsError
from base.service import BaseService
from container.model import Container
from container.model import ContainerType as ct
from container.service import ContainerService
from helpers.search import Pagination
from post.model import Post
from post.repository import PostRepository
from post.schemas import PostAllows, PostCreate, PostUpdate, TopPostShow
from post.utils import generate_slug
from sqlalchemy.ext.asyncio import AsyncSession

from user.model import User


class PostService(BaseService[Post, PostRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session, PostRepository)
        self.container_service = ContainerService(session=session)


    async def create_post(self, author_id: int, post: PostCreate) -> Post:

        post = await self.create_item(
            **post.model_dump(),
            author_id=author_id
        )

        slug = generate_slug(post.title, post.id)

        await self.update_item(post, slug=slug)

        return post

    async def get_top_of_posts(self, q: str):

        posts = await self.repository.get_top_of_posts(q)
        return [TopPostShow(post=post, count=count) for post, count in posts]


    async def update_post(self, post: Post, post_update: PostUpdate) -> Post:

        await self.update_item(post, **post_update.model_dump())

        return post

    async def get_user_posts(self, user: User, pagination: Pagination) -> list[Post]:
        return await self.get_items_by(
            author_id=user.id,
            container_id=None,
            pagination=pagination
        )
