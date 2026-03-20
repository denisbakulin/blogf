from typing import Annotated

from base.db import getSessionDep
from entities.container import Container, ContainerType
from deps.container import get_container
from fastapi import Depends
from services.topic import TopicService


def get_topic_service(
        session: getSessionDep
) -> TopicService:
    return TopicService(session=session)

topicServiceDep = Annotated[TopicService, Depends(get_topic_service)]


topicDep = Annotated[Container, Depends(get_container(type_=ContainerType.TOPIC))]






