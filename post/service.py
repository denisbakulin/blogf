from sqlalchemy.ext.asyncio import AsyncSession
from post.repository import PostRepository
from post.schemas import PostCreate
from user.models import User
from post.models import Post
from post.exceptions import PostNotFoundErr


class PostService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.post_repo = PostRepository(session)

    async def create_post(self, user: User, post_info: PostCreate) -> Post:

        post = self.post_repo.create_post(post_info.model_dump(), author_id=user.id)

        await self.session.commit()

        return post

    async def get_post_by_id(self, post_id: int) -> Post:
        post = await self.post_repo.get_post(post_id=post_id)

        if not post:
            raise PostNotFoundErr(f"Пост с id={post_id} не найден")

        return post

    async def get_posts_by_title(self, title: str, offset: int, limit: int) -> list[Post]:

        posts = await self.post_repo.get_posts(title=title, offset=offset, limit=limit)

        if not posts:
            raise PostNotFoundErr(f"Посты с title={title} не найдены")

        return posts

    async def get_posts_by_slug(self, slug: str, offset: int, limit: int) -> list[Post]:

        posts = await self.post_repo.get_posts(offset=offset, limit=limit)

        if not posts:
            raise PostNotFoundErr(f"Посты с slug={slug} не найдены")

        return posts

    async def get_posts_by_author_username(self, username: str, offset: int, limit: int) -> list[Post]:

        posts = await self.post_repo.get_posts(author_username=username, offset=offset, limit=limit)

        if not posts:
            raise PostNotFoundErr(f"Посты автора={username} не найдены")

        return posts

    async def get_posts_by_author_id(self, user_id: int, offset: int, limit: int) -> list[Post]:

        posts = await self.post_repo.get_posts(author_id=user_id, offset=offset, limit=limit)

        if not posts:
            raise PostNotFoundErr(f"Посты автора id={user_id} не найдены")

        return posts