from __future__ import annotations

import json
import logging
from datetime import date
from pathlib import Path

logger = logging.getLogger(__name__)

_FEEDBACK_DIR = Path(__file__).parents[3] / "data" / "feedback"


class FeedbackCollector:
    def __init__(self, feedback_dir: Path | None = None) -> None:
        self._dir = feedback_dir or _FEEDBACK_DIR
        self._dir.mkdir(parents=True, exist_ok=True)

    def _today_path(self) -> Path:
        return self._dir / f"feedback_{date.today().isoformat()}.jsonl"

    def record(self, text: str, predicted_spam: bool, is_spam: bool, confidence: float, source: str = "user") -> None:
        entry = {
            "text": text,
            "predicted_spam": predicted_spam,
            "is_spam": is_spam,
            "label": 1 if is_spam else 0,
            "confidence": confidence,
            "source": source,
            "date": date.today().isoformat(),
        }
        try:
            with self._today_path().open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError:
            logger.exception("Failed to write feedback entry")

    def get_training_pairs(self, days_back: int = 30) -> tuple[list[str], list[int]]:
        texts: list[str] = []
        labels: list[int] = []

        for path in sorted(self._dir.glob("feedback_*.jsonl"))[-days_back:]:
            try:
                with path.open(encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        entry = json.loads(line)
                        texts.append(entry["text"])
                        labels.append(entry["label"])
            except (OSError, json.JSONDecodeError):
                logger.warning("Failed to read feedback file", extra={"path": str(path)})

        return texts, labels

    def total_samples(self) -> int:
        total = 0
        for path in self._dir.glob("feedback_*.jsonl"):
            try:
                with path.open(encoding="utf-8") as f:
                    total += sum(1 for line in f if line.strip())
            except OSError:
                pass
        return total
