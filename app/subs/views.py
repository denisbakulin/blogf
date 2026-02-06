from fastapi import APIRouter, Depends

from auth.deps import currentUserDep
from helpers.search import Pagination
from post.deps import postServiceDep
from post.schemas import PostShow
from subs.deps import subscribeServiceDep
from subs.schemas import ListOfSubscribes, subscribe_type



subs_router = APIRouter(prefix="/subs", tags=["🔔 Подписки"])


@subs_router.get(
    "",
    summary="Получить подписки пользователя",
    response_model=ListOfSubscribes
)
async def get_subs(
        user: currentUserDep,
        subscribe_service: subscribeServiceDep,
):
    return await subscribe_service.get_subs(user=user)


@subs_router.post(
    "",
    summary="Подписаться/отписаться на пользователя/топик"
)
async def process_subscribe(
        user: currentUserDep,
        sub_type: subscribe_type,
        entity_id: int,
        subscribe_service: subscribeServiceDep,
):
     await subscribe_service.process_subscribe(
        user=user, sub_type=sub_type, entity_id=entity_id
     )


@subs_router.get(
    "/content",
    summary="Получить контент подписок",
    response_model=list[PostShow]
)
async def get_subs_content(
        user: currentUserDep,
        subscribe_service: subscribeServiceDep,
        sub_type: subscribe_type | None = None,
        pagination: Pagination = Depends(),
):
    return await subscribe_service.get_content(
        user=user, sub_type=sub_type, pagination=pagination
    )



