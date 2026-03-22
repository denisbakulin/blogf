from deps.auth import currentUserDep
from deps.subscribe import subscribeServiceDep
from fastapi import APIRouter, Depends
from helpers.search import Pagination
from schemas.post import PostFullShow, PostContainerShow, PostShow
from schemas.container import ContainerShow, ContainerMetricsShow

router = APIRouter(prefix="/subscribes", tags=["🔔 Подписки"])


@router.get(
    "",
    summary="Получить подписки пользователя",
    response_model=list[ContainerMetricsShow]
)
async def get_subs(
        user: currentUserDep,
        service: subscribeServiceDep,
        pagination: Pagination = Depends(),
):
    return await service.get_subs(user_id=user.id, pagination=pagination)



@router.get(
    "/content",
    summary="Получить контент подписок",
    response_model=list[PostContainerShow]
)
async def get_subs_content(
        user: currentUserDep,
        service: subscribeServiceDep,
        pagination: Pagination = Depends(),
):
    content = await service.get_content(
        user_id=user.id, pagination=pagination
    )

    return [
        PostContainerShow(
            **PostShow.from_orm(post).model_dump(),
            container=ContainerShow.from_orm(container)
        ) for post, container in content
    ]



