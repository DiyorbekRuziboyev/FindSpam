from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from core.db.enums import NotificationType, ThreatLevel


class NotificationEvent(BaseModel):
    id: UUID
    event_type: NotificationType
    threat_level: ThreatLevel | None
    message: str
    payload: dict[str, object]
    created_at: datetime


class WebSocketMessage(BaseModel):
    type: str
    room: str
    data: dict[str, object]


class SubscribeRequest(BaseModel):
    rooms: list[str]
