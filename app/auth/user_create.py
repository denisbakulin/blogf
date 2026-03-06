from sqlalchemy.ext.asyncio import AsyncSession

from entities import ContainerType, User
from services.user import UserService
from services.container import ContainerService


class UserCreator:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_s = UserService(self.session)
        self.container_s = ContainerService(self.session)

    async def execute(self, name: str, username: str) -> User:

        user = await self.user_s.create_user(name=name, username=username)

        await self.container_s.create_item(
            author_id=user.id, type=ContainerType.wall, title=f"user[{user.id}]-wall"
        )

        return user
