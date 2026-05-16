from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class AnalyticsSnapshotResponse(BaseModel):
    id: UUID
    snapshot_date: date
    total_messages: int
    spam_detected: int
    scam_detected: int
    phishing_detected: int
    clean_messages: int
    avg_confidence: float
    total_bans: int
    total_warnings: int
    total_deletions: int
    by_language: dict[str, int] | None
    by_category: dict[str, int] | None
    by_threat_level: dict[str, int] | None
    created_at: datetime

    model_config = {"from_attributes": True}


class DashboardSummaryResponse(BaseModel):
    total_messages_today: int
    spam_detected_today: int
    active_threats: int
    bans_today: int
    avg_confidence_today: float
    threat_trend: list[dict[str, object]]
    top_spam_categories: list[dict[str, object]]
    recent_high_confidence_detections: int


class TrendPoint(BaseModel):
    date: date
    spam_count: int
    scam_count: int
    phishing_count: int
    clean_count: int
    total: int


class TrendResponse(BaseModel):
    period_days: int
    data: list[TrendPoint]


class LanguageBreakdownItem(BaseModel):
    language: str
    count: int
    percentage: float


class CategoryBreakdownItem(BaseModel):
    category: str
    count: int
    percentage: float
    avg_confidence: float
