from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from admin.repository import AdminRepository
from admin.exceptions import NotFoundErr, ItemUpdateErr, ItemCreateErr


class AdminService[T]:
    def __init__(self, model: T, session: AsyncSession):
        self.repo = AdminRepository[T](session=session, model=model)
        self.model = model
        self.session = session

    async def get_item_by_id(self, item_id: int) -> T:
        item = await self.repo.get_item_by_id(item_id)

        if not item:
            raise NotFoundErr(f"{self.model} id={item} не найдено!")

        return item

    async def create_item(self, item_create) -> T:
        try:
            item = await self.repo.create_item(item_create.model_dump())

            await self.session.commit()
            await self.session.refresh(item)

            return item

        except SQLAlchemyError as e:
            raise ItemCreateErr(str(e))


    async def update_item(self, item_id: int, update_info) -> T:
        try:
            item = await self.repo.get_item_by_id(item_id)

            await self.repo.update_item(item, update_info.model_dump(exclude_none=True))

            await self.session.commit()
            await self.session.refresh(item)

            return item

        except SQLAlchemyError as e:
            raise ItemUpdateErr(str(e))



