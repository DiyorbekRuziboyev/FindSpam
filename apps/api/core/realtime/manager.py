import asyncio
from collections import defaultdict

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self) -> None:
        self._rooms: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, ws: WebSocket, room: str) -> None:
        await ws.accept()
        self._rooms[room].add(ws)

    def disconnect(self, ws: WebSocket, room: str) -> None:
        self._rooms[room].discard(ws)

    async def broadcast(self, room: str, message: dict) -> None:
        dead: set[WebSocket] = set()
        for ws in self._rooms.get(room, set()):
            try:
                await ws.send_json(message)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self._rooms[room].discard(ws)


ws_manager = WebSocketManager()
