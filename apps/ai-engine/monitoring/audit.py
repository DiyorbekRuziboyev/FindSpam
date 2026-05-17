from __future__ import annotations

import hashlib
import json
import logging
from datetime import date, datetime
from pathlib import Path

logger = logging.getLogger(__name__)

_AUDIT_DIR = Path(__file__).parents[1] / "data" / "audit"


class PredictionAuditor:
    """Append-only JSONL audit trail for every prediction.

    Stores text_hash (SHA-256) rather than raw text to preserve privacy.
    Files rotate daily: audit_YYYY-MM-DD.jsonl
    """

    def __init__(self, audit_dir: Path | None = None) -> None:
        self._dir = audit_dir or _AUDIT_DIR
        self._dir.mkdir(parents=True, exist_ok=True)

    def _today_path(self) -> Path:
        return self._dir / f"audit_{date.today().isoformat()}.jsonl"

    @staticmethod
    def _hash_text(text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    def record(
        self,
        text: str,
        is_spam: bool,
        confidence: float,
        threat_level: str,
        spam_category: str | None,
        model_contributions: dict[str, float],
        processing_ms: float,
        metadata: dict | None = None,
    ) -> None:
        entry = {
            "text_hash": self._hash_text(text),
            "text_length": len(text),
            "is_spam": is_spam,
            "confidence": round(confidence, 4),
            "threat_level": threat_level,
            "spam_category": spam_category,
            "model_contributions": {k: round(v, 4) for k, v in model_contributions.items()},
            "processing_ms": round(processing_ms, 2),
            "metadata": metadata or {},
            "audited_at": datetime.utcnow().isoformat(),
        }
        try:
            with self._today_path().open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError:
            logger.exception("Failed to write audit entry")

    def tail(self, n: int = 100) -> list[dict]:
        path = self._today_path()
        if not path.exists():
            return []
        lines: list[str] = []
        try:
            with path.open(encoding="utf-8") as f:
                lines = f.readlines()
        except OSError:
            return []
        entries = []
        for line in lines[-n:]:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return entries
