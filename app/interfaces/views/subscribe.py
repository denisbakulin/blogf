from deps.auth import currentUserDep
from deps.subscribe import subscribeServiceDep
from fastapi import APIRouter, Depends
from helpers.search import Pagination
from schemas.post import PostShow


subs_router = APIRouter(prefix="/subs", tags=["🔔 Подписки"])


@subs_router.get(
    "",
    summary="Получить подписки пользователя",
)
async def get_subs(
        user: currentUserDep,
        service: subscribeServiceDep,
        pagination: Pagination = Depends(),
):
    return await service.get_subs(user_id=user.id, pagination=pagination)



@subs_router.get(
    "/content",
    summary="Получить контент подписок",
)
async def get_subs_content(
        user: currentUserDep,
        service: subscribeServiceDep,
        pagination: Pagination = Depends(),
):
    return await service.get_content(
        user_id=user.id, pagination=pagination
    )



