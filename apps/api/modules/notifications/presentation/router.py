import structlog
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from core.realtime.manager import ws_manager
from core.security.dependencies import AuthenticatedUser, get_current_user

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.websocket("/ws")
async def notifications_ws(
    websocket: WebSocket,
    token: str,
) -> None:
    """Realtime notification stream. Pass JWT as ?token= query param."""
    from core.security.jwt import decode_access_token

    try:
        payload = decode_access_token(token)
    except Exception:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    user_id = payload.get("sub", "anonymous")
    room = f"user:{user_id}"

    await ws_manager.connect(websocket, room)
    logger.info("ws_client_connected", user_id=user_id, room=room)

    try:
        while True:
            # Keep-alive — clients may send pings; discard payload
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, room)
        logger.info("ws_client_disconnected", user_id=user_id, room=room)


@router.websocket("/ws/admin")
async def admin_notifications_ws(
    websocket: WebSocket,
    token: str,
) -> None:
    """Admin-only realtime feed (moderation queue, threat alerts)."""
    from core.db.enums import UserRole
    from core.security.jwt import decode_access_token

    try:
        payload = decode_access_token(token)
    except Exception:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    role = payload.get("role")
    if role not in {UserRole.SUPER_ADMIN, UserRole.ADMIN}:
        await websocket.close(code=4003, reason="Forbidden")
        return

    await ws_manager.connect(websocket, "admin")
    logger.info("ws_admin_connected", user_id=payload.get("sub"))

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "admin")


@router.get("/channels", summary="List available notification rooms")
async def list_channels(
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> dict[str, list[str]]:
    return {
        "rooms": [
            f"user:{current_user.id}",
            "admin",
            "moderation",
            "ai-predictions",
        ]
    }
