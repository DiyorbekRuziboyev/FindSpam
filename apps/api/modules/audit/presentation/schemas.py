from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from core.db.enums import ActorType


class AuditLogListItem(BaseModel):
    id: UUID
    actor_type: ActorType
    actor_id: str | None
    action: str
    resource_type: str
    resource_id: str | None
    ip_address: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AuditLogDetail(AuditLogListItem):
    old_value: str | None
    new_value: str | None
    metadata: dict[str, object] | None


class AuditLogFilter(BaseModel):
    actor_type: ActorType | None = None
    actor_id: str | None = None
    action: str | None = None
    resource_type: str | None = None
    resource_id: str | None = None


class AuditSummaryResponse(BaseModel):
    total_events: int
    events_today: int
    by_actor_type: dict[str, int]
    by_action: dict[str, int]
    top_resources: list[dict[str, object]]
