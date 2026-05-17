from __future__ import annotations

import asyncio
import logging

from core.training.base import TrainingConfig, TrainingResult
from core.training.feedback_collector import FeedbackCollector

logger = logging.getLogger(__name__)

_RETRAIN_THRESHOLD = 500


class RetrainingPipeline:
    def __init__(
        self,
        tfidf_lr_adapter=None,
        feedback_collector: FeedbackCollector | None = None,
        retrain_threshold: int = _RETRAIN_THRESHOLD,
    ) -> None:
        self._adapter = tfidf_lr_adapter
        self._collector = feedback_collector or FeedbackCollector()
        self._retrain_threshold = retrain_threshold

    def should_retrain(self) -> bool:
        return self._collector.total_samples() >= self._retrain_threshold

    def _sync_retrain(self) -> TrainingResult | None:
        from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
        from sklearn.model_selection import train_test_split

        texts, labels = self._collector.get_training_pairs()
        if len(texts) < self._retrain_threshold:
            logger.info("Not enough feedback samples for retraining", extra={"samples": len(texts)})
            return None

        config = TrainingConfig(model_name="tfidf_lr")
        x_train, x_test, y_train, y_test = train_test_split(
            texts, labels, test_size=config.test_size, random_state=config.random_state, stratify=labels
        )

        if self._adapter is None:
            logger.warning("No TF-IDF+LR adapter configured; retraining skipped")
            return None

        self._adapter.train(x_train, y_train)

        from sklearn.pipeline import Pipeline

        pipeline = self._adapter._pipeline
        y_pred = pipeline.predict(x_test)

        result = TrainingResult(
            model_name="tfidf_lr",
            accuracy=accuracy_score(y_test, y_pred),
            f1_score=f1_score(y_test, y_pred, average="binary"),
            precision=precision_score(y_test, y_pred, average="binary"),
            recall=recall_score(y_test, y_pred, average="binary"),
            samples_used=len(texts),
        )
        logger.info(
            "Retraining complete",
            extra={
                "model": result.model_name,
                "accuracy": result.accuracy,
                "f1": result.f1_score,
                "samples": result.samples_used,
            },
        )
        return result

    async def run(self) -> TrainingResult | None:
        if not self.should_retrain():
            return None
        logger.info("Starting retraining pipeline", extra={"threshold": self._retrain_threshold})
        return await asyncio.to_thread(self._sync_retrain)
