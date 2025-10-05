from typing import Optional, Type

from fastapi import APIRouter, Depends

from admin.deps import get_admin_service
from admin.schemas import AdminUserCreate, AdminUserShow, AdminUserUpdate
from admin.service import AdminService
from auth.deps import get_admin
from core.model import BaseORM, ColumnProps
from core.schemas import BaseSchema
from post.model import Post
from user.model import User


class Admin(APIRouter):
    """Главный админ-роут с проверкой на права администратора"""

    def __init__(self, *routers):
        super().__init__(
            dependencies=[Depends(get_admin)],
            prefix="/admin",
            tags=["admin"],
        )
        if routers:
            for router in routers:
                self.include_router(router)


class AdminView(APIRouter):
    """
    Класс-родитель для написания админ-роутов

    пример:

    class ExampleAdminView(AdminView, model=example, delete_=False):
        def init_custom_views():
            ...

    """
    # модель ORM с которой будет взаимодействовать админка
    model: Type[BaseORM] = None

    # удаление записи
    delete_: bool = False

    # Схема для демонстрации записи
    show: Type[BaseSchema] = None

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
        model_name = model.__name__


        self.get(
            "/table-info",
            response_model=list[ColumnProps],
            summary=f"Получить информацию о таблице {model_name}"
        )(model.table_info)

        @self.get(
            "/count",
            response_model=int,
            summary=f"Получить количество записей {model_name}"
        )
        async def get_item_count(
                admin_service: AdminService = Depends(get_admin_service(model=model))
        ):
            return await admin_service.get_items_count()


        async def get_item(
                item_id: int,
                admin_service: AdminService = Depends(get_admin_service(model=model))
        ):
            return await admin_service.get_item_by_id(item_id)

        async def delete_item(
                item_id: int,
                admin_service: AdminService = Depends(get_admin_service(model=model))
        ):
            return await admin_service.delete_item_by_id(item_id)

        if self.show:
            self.get(
                "/{item_id}",
                response_model=self.show,
                summary=f"Получить {model_name} по id"
            )(get_item)

        if self.delete_:
            self.delete(
                "/{item_id}",
                summary=f"Удалить {model_name} по id"
            )(delete_item)



    def init_custom_views(self):
        """В этом методе прописываются кастомные
        роуты с отличной от изночальной логикой

        @self.get("path"): ...
        """


from admin.schemas import AdminPostShow
from user.deps import userServiceDep


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













