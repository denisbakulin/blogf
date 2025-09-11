from fastapi import APIRouter, Depends, HTTPException
from user.models import User
from admin.schemas import AdminUserShow, AdminUserUpdate, AdminUserCreate
from core.models import BaseORM, ColumnProps
from core.schemas import BaseSchema


from admin.service import AdminService
from admin.dependencies import get_admin_service
from admin.exceptions import NotFoundErr, ItemUpdateErr, ItemCreateErr

from auth.dependencies import get_admin
from post.models import Post


from typing import Type, Optional

class AdminView(APIRouter):
    model: Type[BaseORM] = None
    delete_: bool = False
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
            try:
                return await admin_service.get_item_by_id(item_id)
            except NotFoundErr as e:
                raise HTTPException(404, str(e))

        def get_table_info():
            return model.table_info()

        async def create_item(
                item_create: create,
                admin_service: AdminService = Depends(get_admin_service(model=model))
        ):
            try:
                item = await admin_service.create_item(item_create)
                return item
            except ItemCreateErr as e:
                raise HTTPException(409, str(e))

        async def update_item(
                item_id: int,
                update_data: update,
                admin_service: AdminService = Depends(get_admin_service(model=model))
        ):
            try:
                return await admin_service.update_item(item_id, update_data)
            except NotFoundErr as e:
                raise HTTPException(404, str(e))
            except ItemUpdateErr as e:
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
            self.delete("")(delete_item)

        self.get("/table-info", response_model=list[ColumnProps])(get_table_info)

    def init_custom_views(self):
        ...

from user.dependencies import userServiceDep
from user.exceptions import UserAlreadyExistErr, UserNotFoundErr


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
            try:
                return await user_service.create_user(user_create)
            except UserAlreadyExistErr as e:
                raise HTTPException(401, str(e))
        @self.patch("/{user_id}")
        async def update_user(
                user_id: int,
                user_data: AdminUserUpdate,
                user_service: userServiceDep
        ):
            try:
                user = await user_service.get_user_by_id(user_id)
                return await user_service.update_user(user, user_data)
            except UserNotFoundErr as e:
                raise HTTPException(404, str(e))

            except UserAlreadyExistErr as e:
                raise HTTPException(404, str(e))



from admin.schemas import AdminPostCreate, AdminPostUpdate, AdminPostShow



class PostAdminView(AdminView, model=Post, delete_=True):
    show = AdminPostShow
    update = AdminPostUpdate
    create = AdminPostCreate


class Admin(APIRouter):

    def __init__(self, *routers):
        super().__init__(
            dependencies=[Depends(get_admin)],
            prefix="/admin",
            tags=["admin"]
        )
        if routers:
            for router in routers:
                self.include_router(router)








