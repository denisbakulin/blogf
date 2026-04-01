from base.db import getSessionDep
from deps.auth import currentUserDep

from deps.topic import topicServiceDep
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination

from schemas.topic import ContainerMetricsShow, CreateTopic, TopicShow, UserUsername
from logic import CreateTopicUseCase
from utils.container import ContainerSearchParams

router = APIRouter(prefix="/topics", tags=["📚 Темы"])


@router.get(
    "",
    summary="Получить темы",
    response_model=list[TopicShow]
)
async def get_topics(
        service: topicServiceDep,
        pagination: Pagination = Depends()
):
    topics = await service.get_topics(pagination=pagination)

    return [
        TopicShow(
            **ContainerMetricsShow.from_orm(topic).model_dump(),
            author=UserUsername.from_orm(author)
        ) for topic, author in topics
    ]



@router.post(
    "",
    summary="Создать тему",
    status_code=status.HTTP_201_CREATED,
)
async def create_topic(
    create: CreateTopic,
    session: getSessionDep,
    user: currentUserDep
):
    logic = CreateTopicUseCase(session)

    return await logic.execute(user=user, create=create)





@router.get(
    "/search",
    summary="Поиск темы по ключевым параметрам",
)
async def search_topics(
    service: topicServiceDep,
    pagination: Pagination = Pagination(),
    search: ContainerSearchParams = Depends(),
):
    return await service.search_topic(search=search, pagination=pagination)



@router.get(
    "/{topic_id}",
    summary="Получить тему",
    response_model=TopicShow
)
async def get_topic(
        topic_id: int,
        service: topicServiceDep
):
    topic, author = await service.get_full_topic(topic_id)

    return TopicShow(
        **ContainerMetricsShow.from_orm(topic).model_dump(),
        author=UserUsername.from_orm(author)
    )






