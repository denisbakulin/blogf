from fastapi import APIRouter, Depends
from user.deps import userDep
from auth.deps import currentUserDep
from subs.deps import subscribeServiceDep
from helpers.search import Pagination
from post.schemas import PostShow

subs_router = APIRouter(prefix="/subs", tags=["🔔 Подписки"])

from subs.schemas import SubscribeShow
from post.deps import postServiceDep

@subs_router.get(
    "",
    summary="Получить подписки пользователя",
    response_model=list[SubscribeShow]
)
async def get_subs(
        user: currentUserDep,
        subscribe_service: subscribeServiceDep,
        pagination: Pagination = Depends()
):
    return await subscribe_service.get_user_subscribes(user, pagination)


@subs_router.get(
    "/content",
    summary="Получить контент подписок",
    response_model=list[PostShow]
)
async def get_subs_content(
        user: currentUserDep,
        post_service: postServiceDep,
        pagination: Pagination = Depends()
):
    return await post_service.repository.get_posts_by_user_subscribes(user.id, **pagination.get())


@subs_router.post(
    "/{username}",
    summary="Подписаться/отписаться на пользователя",
    response_model=SubscribeShow
)
async def subscribe(
        user: currentUserDep,
        creator: userDep,
        subscribe_service: subscribeServiceDep,
):
    return await subscribe_service.process_subscribe(user, creator)





