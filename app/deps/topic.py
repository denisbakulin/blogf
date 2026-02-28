from typing import Annotated

from base.db import getSessionDep
from fastapi import Depends
from entities.container import Container
from services.topic import TopicService


def get_topic_service(
        session: getSessionDep
) -> TopicService:
    return TopicService(session=session)

topicServiceDep = Annotated[TopicService, Depends(get_topic_service)]

async def get_topic(
        slug: str,
        topic_service: topicServiceDep,
) -> Container:
    return await topic_service.container_service.get_full_container(slug=slug)


topicDep = Annotated[Container, Depends(get_topic)]






