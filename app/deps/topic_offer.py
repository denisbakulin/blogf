from typing import Annotated

from fastapi import Depends

from base.db import getSessionDep
from entities.topic_offer import TopicOffer
from services.topic_offer import TopicOfferService


def get_topic_offer_service(
        session: getSessionDep
) -> TopicOfferService:
    return TopicOfferService(session=session)

topicOfferServiceDep = Annotated[TopicOfferService, Depends(get_topic_offer_service)]


async def get_offer_topic(
        service: topicOfferServiceDep,
        offer_id: int
):
    return await service.get_item_by_id(offer_id)


offerTopicDep = Annotated[TopicOffer, Depends(get_offer_topic)]
