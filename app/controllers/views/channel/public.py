from base.db import getSessionDep
from deps.auth import currentUserDep
from fastapi import APIRouter, status
from services.subscribe import SubscribeService
from services.channel import PublicChannelService


router = APIRouter(prefix="/{channel_id}", tags=["Public channel"])

@router.post(
    "/subscribe",
    summary="Подписаться на публичный канал",
    status_code=status.HTTP_201_CREATED
)
async def create_subscribe(
    channel_id: int,
    session: getSessionDep,
    user: currentUserDep,
):
    channel_service = PublicChannelService(session)
    subscribe_service = SubscribeService(session)

    channel = await channel_service.get_channel(channel_id)

    return await subscribe_service.create_subscribe(
        user_id=user.id, container_id=channel.id
    )