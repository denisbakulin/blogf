from typing import Annotated

from base.db import getSessionDep
from fastapi import Depends
from topic.offrer.model import TopicOffer
from topic.release.service import TopicOfferService, TopicService
from container.model import Container
from container.service import ContainerService

def get_topic_service(
        session: getSessionDep
) -> TopicService:
    return TopicService(session=session)

def get_topic_offer_service(
        session: getSessionDep
) -> TopicOfferService:
    return TopicOfferService(session=session)


topicServiceDep = Annotated[TopicService, Depends(get_topic_service)]
topicOfferServiceDep = Annotated[TopicOfferService, Depends(get_topic_offer_service)]


async def get_topic(
        slug: str,
        topic_service: topicServiceDep,
) -> Container:
    return await topic_service.get_item_by(slug=slug)

async def get_topic_offer(
        offer_id: int,
        topic_service: topicOfferServiceDep
) -> TopicOffer:
    return await topic_service.get_item_by_id(offer_id)



async def get_container_service(
    session: getSessionDep
) -> ContainerService:
    return ContainerService(session=session)


topicOfferDep = Annotated[TopicOffer, Depends(get_topic_offer)]
containerServiceDep = Annotated[ContainerService, Depends(get_container_service)]
topicDep = Annotated[Container, Depends(get_topic)]



