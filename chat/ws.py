from fastapi import Query, APIRouter
from fastapi.websockets import WebSocketDisconnect, WebSocket
from chat.manager import WebSocketManager
from auth.utils import decode_token
from chat.schemas import ClientDirectEvent


direct_manager = WebSocketManager()

ws = APIRouter(prefix="/ws")

@ws.websocket("/ws")
async def websocket_actions(
        websocket: WebSocket,
        token: str = Query(...),
):
    token_info = decode_token(token)

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