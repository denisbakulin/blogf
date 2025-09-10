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

class AdminView(APIRouter):
    model: BaseORM = None
    show_schema: BaseSchema = None
    update_schema: BaseSchema = None
    create_schema: BaseSchema = None

    def __init__(self):
        tablename = self.model.__tablename__
        super().__init__(
            prefix=f"/{tablename}",
            tags=[f"Admin - {tablename}"]
        )
        self.init_router()

    def __init_subclass__(cls, /, model, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.model = model


    def init_router(self):
        model = self.model
        show_schema = self.show_schema
        update_schema = self.update_schema
        create_schema = self.create_schema

        if not all([model, show_schema, update_schema, create_schema]):
            raise ValueError()


        @self.get(
            f"",
            response_model=show_schema
        )
        async def get_item(
                item_id: int,
                admin_service: AdminService = Depends(get_admin_service(model=model))
        ):
            try:
                return await admin_service.get_item_by_id(item_id)
            except NotFoundErr as e:
                raise HTTPException(404, str(e))

        @self.get(
            "/table-info",
            response_model=list[ColumnProps]
        )
        def gettable_info():
            return model.table_info()


        @self.post(
            "",
            response_model=show_schema
        )
        async def create_item(
                item_create: create_schema,
                admin_service: AdminService = Depends(get_admin_service(model=model))
        ):
            try:
                item = await admin_service.create_item(item_create)
                print(User.table_info())
                return item
            except ItemCreateErr as e:
                raise HTTPException(409, str(e))

        @self.patch(
            f"",
            response_model=self.show_schema
        )
        async def update_item(
                item_id: int,
                update_data: update_schema,
                admin_service: AdminService = Depends(get_admin_service(model=model))
        ):
            try:
                return await admin_service.update_item(item_id, update_data)
            except ItemUpdateErr as e:
                raise HTTPException(409, str(e))


    def get_item_by_id(self, item_id: int):
        ...

    def del_item(self, item_id):
        print(self.model, self.show_schema)


class UserAdminView(AdminView, model=User):
    show_schema = AdminUserShow
    update_schema = AdminUserUpdate
    create_schema = AdminUserCreate


class PostAdminView(AdminView, model=Post):
    show_schema = AdminUserShow
    update_schema = AdminUserUpdate
    create_schema = AdminUserCreate

class Admin(APIRouter):

    def __init__(self):
        super().__init__(
            dependencies=[Depends(get_admin)],
            prefix="/admin",
            tags=["admin"]
        )






