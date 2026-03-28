from typing import Annotated

from base.db import getSessionDep
from fastapi import Depends
from services.topic import TopicService


def get_topic_service(
        session: getSessionDep
) -> TopicService:
    return TopicService(session=session)

topicServiceDep = Annotated[TopicService, Depends(get_topic_service)]







