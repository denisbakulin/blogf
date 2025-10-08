from typing import Optional, Type

from fastapi import APIRouter, Depends

from admin.deps import get_admin_service
from admin.schemas import  AdminUserShow, AdminUserUpdate, UserFields
from admin.service import AdminService
from auth.deps import get_admin
from core.model import BaseORM, ColumnProps
from core.schemas import BaseSchema
from post.model import Post
from user.model import User
from user.schemas import UserCreate

class Admin(APIRouter):
    """Главный админ-роут с проверкой на права администратора"""

    def __init__(self, *routers, **kwargs):

        super().__init__(
            dependencies=[Depends(get_admin)],
            prefix="/admin",
            **kwargs
        )
        if routers:
            for router in routers:
                self.include_router(router, include_in_schema=True)

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
        self.root_path = self.model.__tablename__
        self.table_name = table_name

        table_name = table_name or self.root_path
        tags = tags or [f"⚙ Админ - {table_name}"]

        super().__init__(
            prefix=f"/{self.root_path}",
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



        self.get(
            "/table-info",
            response_model=list[ColumnProps],
            summary=f"Получить информацию о таблице {self.table_name}"
        )(model.table_info)

        @self.get(
            "/count",
            response_model=int,
            summary=f"Получить количество записей {self.table_name}"
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
                summary=f"Получить {self.table_name} по id"
            )(get_item)

        if self.delete_:
            self.delete(
                "/{item_id}",
                summary=f"Удалить {self.table_name} по id"
            )(delete_item)



    def init_custom_views(self):
        """В этом методе прописываются кастомные
        роуты с отличной от изночальной логикой

        @self.get("path"): ...
        """


from user.schemas import UserShowMe
from user.deps import userServiceDep, userDep


class UserAdminView(AdminView, model=User):
    show = UserShowMe

    def init_custom_views(self):

        @self.post(
            "",
            summary="Создать пользователя",
            response_model=self.show
        )
        async def create_user(
                user_create: UserCreate,
                user_service: userServiceDep,
                extra: UserFields = Depends(),

        ):
            return await user_service.create_user(user_create, **extra.dict())


        @self.patch(
            "/{username}",
            summary="Изменить пользователя"
        )
        async def update_user(
                user: userDep,
                user_data: AdminUserUpdate,
                user_service: userServiceDep
        ):
            return await user_service.update_user(user, user_data)



from post.schemas import PostShow


class PostAdminView(AdminView, model=Post, delete_=True):
    show = PostShow

    def init_custom_views(self):
       ...













