from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PredictionRecord:
    is_spam: bool
    confidence: float
    threat_level: str
    processing_ms: float
    recorded_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class MetricsSummary:
    total_predictions: int
    spam_count: int
    spam_rate: float
    avg_confidence: float
    avg_latency_ms: float
    high_threat_count: int
    p95_latency_ms: float


class InferenceMetrics:
    def __init__(self, window_size: int = 1000) -> None:
        self._window: deque[PredictionRecord] = deque(maxlen=window_size)
        self._total_predictions: int = 0
        self._lock = threading.Lock()

    def record(self, is_spam: bool, confidence: float, threat_level: str, processing_ms: float) -> None:
        record = PredictionRecord(
            is_spam=is_spam,
            confidence=confidence,
            threat_level=threat_level,
            processing_ms=processing_ms,
        )
        with self._lock:
            self._window.append(record)
            self._total_predictions += 1

    def summary(self) -> MetricsSummary:
        with self._lock:
            records = list(self._window)

        if not records:
            return MetricsSummary(
                total_predictions=self._total_predictions,
                spam_count=0,
                spam_rate=0.0,
                avg_confidence=0.0,
                avg_latency_ms=0.0,
                high_threat_count=0,
                p95_latency_ms=0.0,
            )

        spam_records = [r for r in records if r.is_spam]
        high_threat = [r for r in records if r.threat_level in ("HIGH", "CRITICAL")]
        latencies = sorted(r.processing_ms for r in records)
        p95_idx = max(0, int(len(latencies) * 0.95) - 1)

        return MetricsSummary(
            total_predictions=self._total_predictions,
            spam_count=len(spam_records),
            spam_rate=len(spam_records) / len(records),
            avg_confidence=sum(r.confidence for r in records) / len(records),
            avg_latency_ms=sum(r.processing_ms for r in records) / len(records),
            high_threat_count=len(high_threat),
            p95_latency_ms=latencies[p95_idx],
        )
