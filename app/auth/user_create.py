from entities import ContainerType, User
from services.container import ContainerService
from services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from utils.user import create_username


class UserCreator:
    """Создание пользователя с необходимыми зависимостями"""


    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_s = UserService(self.session)
        self.container_s = ContainerService(self.session)

    async def execute(self, name: str, username: str | None = None) -> User:

        username = username or create_username()
        user = await self.user_s.create_user(name=name, username=username)

        await self.container_s.create_item(
            author_id=user.id, type=ContainerType.WALL, title=f"user[{user.id}]-wall"
        )

        return user
