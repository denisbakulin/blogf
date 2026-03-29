from typing import Annotated

from base.db import getSessionDep
from fastapi import Depends
from services.topic_offer import TopicOfferService


def get_topic_offer_service(
        session: getSessionDep
) -> TopicOfferService:
    return TopicOfferService(session=session)

topicOfferServiceDep = Annotated[TopicOfferService, Depends(get_topic_offer_service)]
