
from fastapi import APIRouter, Depends

allow_router = APIRouter(prefix="/allows", tags=["💬 Права"])
from allows.deps import allowServiceDep
from allows.schema import AllowBase, AllowShow
from helpers.search import Pagination


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









