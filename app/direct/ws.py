from direct.manager import WebSocketManager
from direct.schemas import ClientDirectEvent
from fastapi import APIRouter, Query
from fastapi.websockets import WebSocket, WebSocketDisconnect
from utils.auth import get_decoded_token

direct_manager = WebSocketManager()

ws = APIRouter(prefix="/ws")

@ws.websocket("/ws")
async def websocket_actions(
        websocket: WebSocket,
        token: str = Query(...),
):
    token_info = get_decoded_token(token)

    if token_info.type != "access":
        raise ValueError()

    await websocket.accept()

    try:
        async for event in websocket.iter_json():
            await direct_manager.process(
                ClientDirectEvent(**event, initiator=token_info.user_id)
            )

    except WebSocketDisconnect:
        ...