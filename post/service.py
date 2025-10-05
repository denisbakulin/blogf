from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import EntityBadRequestError
from core.service import BaseService
from helpers.search import Pagination
from post.model import Post
from post.repository import PostRepository
from post.schemas import PostCreate, PostUpdate
from post.utils import PostSearchParams, generate_slug
from user.model import User


class PostService(BaseService):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session, PostRepository)

    async def create_post(self, user: User, post_info: PostCreate) -> Post:

        post = self.repository.create_post(**post_info.model_dump(), author_id=user.id)
        await self.session.commit()

        slug = generate_slug(post.title, post.id)

        await self.update_item(post, slug=slug)

        return post


    async def get_post_by_slug(
            self,
            slug: str,
    ) -> Post:
        return await self.get_item_by(slug=slug)

    async def update_post(self, post: Post, user: User, update_data: PostUpdate) -> Post:

        if post.author_id != user.id:
            raise EntityBadRequestError(
                "Post",
                f"Пост id={post.id} не принадлежит user={user.username}"
            )

        await self.update_item(post, **update_data.model_dump())

        return post


    async def get_posts_by_author_id(
            self,
            author_id: int,
            pagination: Pagination,
    ) -> list[Post]:
        return await self.repository.get_any_by(author_id=author_id, **pagination.get())

    async def search_posts(
            self,
            search: PostSearchParams,
            pagination: Pagination
    ) -> list[Post]:
        return await self.search_items(search, pagination)
