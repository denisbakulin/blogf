from fastapi import APIRouter, Depends

from auth.deps import currentUserDep, role_validate
from comment.deps import commentDep, commentServiceDep
from comment.schemas import CommentShow, CommentUpdate
from user.model import UserRoleEnum

allow_router = APIRouter(prefix="/allows", tags=["💬 Права"])
from allows.schema import AllowShow, AllowBase
from allows.service import AllowService, AllowPostService
from helpers.search import Pagination

from allows.deps import allowServiceDep
@allow_router.get(
    "/",
    response_model=list[AllowShow],
    summary="Получить комментарий по id"
)
async def get_comment(
        service: allowServiceDep,
        pagination: Pagination = Depends()
):
    return await service.get_items_by(pagination=pagination)

@allow_router.post(
    "/",
    response_model=AllowShow,
    summary="Получить комментарий по id"
)
async def get_comment(
        service: allowServiceDep,
        create: AllowBase
):
    return await service.create_allow(user_id=1, **create.dict())









