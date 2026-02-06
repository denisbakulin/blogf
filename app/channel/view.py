from fastapi import APIRouter, Depends
from helpers.search import Pagination

from channel.deps import channelServiceDep

from container.schemas import ContainerShow, FullContainerShow

channel_router = APIRouter(prefix="/channels", tags=["📚 Каналы"])



@channel_router.get(
    "",
    summary="Получить каналы",
    response_model=list[FullContainerShow]
)
async def get_channels(
        service: channelServiceDep,
        pagination: Pagination = Depends()
):
    return await service.container_service.get_full_containers(pagination)





@channel_router.get(
    "/search",
    summary="Поиск пользователя по ключевым параметрам",
    response_model=list[ContainerShow],
)
async def search_topics(
        topic_service: channelServiceDep,
        pagination: Pagination = Pagination(),
   
):
    return await topic_service.search_containers(pagination=pagination)


