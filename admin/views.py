from fastapi import APIRouter, Depends, HTTPException
from user.models import User
from admin.schemas import AdminUserShow, AdminUserUpdate, AdminUserCreate
from core.models import BaseORM, ColumnProps
from core.schemas import BaseSchema


from admin.service import AdminService
from admin.dependencies import get_admin_service

from auth.dependencies import get_admin
from post.models import Post
from sqlalchemy.exc import SQLAlchemyError

from typing import Type, Optional


class AdminView(APIRouter):
    """
    Класс-родитель для написания админ-роутов

    пример:

    class ExampleAdminView(AdminView, model=example, delete_=False):
        show = ShowModel
        update = UpdateModel

    """
    # модель ORM с которой будет взаимодействовать админка
    model: Type[BaseORM] = None

    # удаление сущности
    delete_: bool = False

    # Схемы для взаимодействия с сущностями
    show: Type[BaseSchema] = None
    update: Type[BaseSchema] = None
    create: Type[BaseSchema] = None

    def __init_subclass__(cls, **kwargs):
        for key, value in kwargs.items():
            setattr(cls, key, value)

    def __init__(
        self,
            table_name: Optional[str] = None,
            tags: Optional[list[str]] = None,
            **kwargs
    ):
        #устанавливаем /path и tags[] по дефолту (__tablename__) или аргументу
        table_name = table_name or self.model.__tablename__
        tags = tags or [f"Admin - {table_name}"]

        super().__init__(
            prefix=f"/{table_name}",
            tags=tags,
            **kwargs
        )

        self.init_default_views()
        self.init_custom_views()


    def init_default_views(self):
        """
        Определение дефолтных роутов (простые CRUD без проверок)
        """

        if not self.model:
            raise ValueError()

        model = self.model
        create = self.create
        update = self.update

        params = {
            "path": "/{item_id}",
            "response_model": self.show
        }

        async def get_item(
                item_id: int,
                admin_service: AdminService = Depends(get_admin_service(model=model))
        ):
            return await admin_service.get_item_by_id(item_id)


        def get_table_info():
            return model.table_info()

        async def get_item_count(
                admin_service: AdminService = Depends(get_admin_service(model=model))
        ):
            return await admin_service.get_items_count()

        self.get("/table-info", response_model=list[ColumnProps])(get_table_info)
        self.get("/count", response_model=int)(get_item_count)

        async def create_item(
                item_create: create,
                admin_service: AdminService = Depends(get_admin_service(model=model))
        ):
            try:
                item = await admin_service.create_item(item_create)
                return item
            except SQLAlchemyError as e:
                raise HTTPException(409, str(e))

        async def update_item(
                item_id: int,
                update_data: update,
                admin_service: AdminService = Depends(get_admin_service(model=model))
        ):
            try:
                return await admin_service.update_item(item_id, update_data)
            except SQLAlchemyError as e:
                raise HTTPException(409, str(e))

        async def delete_item(
                item_id: int,
                admin_service: AdminService = Depends(get_admin_service(model=model))
        ):

            return await admin_service.delete_item(item_id)


        if self.show:
            self.get(**params)(get_item)
        if self.create:
            self.post("", response_model=self.show)(create_item)
        if self.update:
            self.patch(**params)(update_item)
        if self.delete_:
            self.delete("/{item_id}")(delete_item)



    def init_custom_views(self):
        """В этом методе прописываются кастомные
        роуты с отличной от изночальной логикой

        @self.get("path"): ...
        """


from user.dependencies import userServiceDep







from admin.schemas import AdminPostCreate, AdminPostUpdate, AdminPostShow


class UserAdminView(AdminView, model=User):
    show = AdminUserShow

    def init_custom_views(self):

        @self.post(
            "",
            response_model=self.show
        )
        async def create_user(
                user_create: AdminUserCreate,
                user_service: userServiceDep
        ):
            return await user_service.create_user(user_create)


        @self.patch("/{user_id}")
        async def update_user(
                user_id: int,
                user_data: AdminUserUpdate,
                user_service: userServiceDep
        ):

            user = await user_service.get_user_by_id(user_id)
            return await user_service.update_user(user, user_data)

class PostAdminView(AdminView, model=Post, delete_=True):
    show = AdminPostShow

    def init_custom_views(self):
       ...




class Admin(APIRouter):
    """Главный админ-роут с проверкой на права администратора"""

    def __init__(self, *routers):
        super().__init__(
            dependencies=[Depends(get_admin)],
            prefix="/admin",
            tags=["admin"]
        )
        if routers:
            for router in routers:
                self.include_router(router)








