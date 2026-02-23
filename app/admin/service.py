from base.exceptions import EntityBadRequestError
from base.repository import BaseRepository
from base.service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from user.model import User, UserRoleEnum
from user.service import UserService


class AdminService[T](BaseService[T, BaseRepository]):
    def __init__(self, model: T, session: AsyncSession):
        super().__init__(model, session)


    async def get_items_count(self) -> int:
        return await self.repository.get_items_count()


class AdminUserService(UserService):

    async def edit_user_role(
            self,
            current: User,
            user: User,
            role: UserRoleEnum
    ) -> User:
        if user.role in (UserRoleEnum.SUPER_ADMIN, UserRoleEnum.ANONYMOUS):
            raise EntityBadRequestError(
                "Права",
                f"Нельзя посенять права пользователя {user.username}"
            )
        if current.role == UserRoleEnum.SUPER_ADMIN:
            if role not in (UserRoleEnum.SUPER_ADMIN, UserRoleEnum.ANONYMOUS):
                return await self.update_item(user, role=role)
            raise EntityBadRequestError(
                "Права",
                f"Нельзя создать пользователя с правами {role}"
            )
        if role in (UserRoleEnum.MODERATOR, UserRoleEnum.USER):
            return await self.update_item(user, role=role)
        raise EntityBadRequestError("Права", "Недостаточно прав!")









