from deps.auth import currentUserDep
from deps.subscribe import subscribeServiceDep
from fastapi import APIRouter, Depends
from helpers.search import Pagination
from schemas.post import PostShow
from schemas.subscribe import ListOfSubscribes, subscribe_type

subs_router = APIRouter(prefix="/subs", tags=["🔔 Подписки"])


@subs_router.get(
    "",
    summary="Получить подписки пользователя",
    response_model=ListOfSubscribes
)
async def get_subs(
        user: currentUserDep,
        service: subscribeServiceDep,
):
    return await service.get_subs(user=user)



@subs_router.get(
    "/content",
    summary="Получить контент подписок",
    response_model=list[PostShow]
)
async def get_subs_content(
        user: currentUserDep,
        service: subscribeServiceDep,
        sub_type: subscribe_type | None = None,
        pagination: Pagination = Depends(),
):
    return await service.get_content(
        user=user, sub_type=sub_type, pagination=pagination
    )



