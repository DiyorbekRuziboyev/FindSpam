from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass

from core.serving.predictor import PredictionResult

logger = logging.getLogger(__name__)


@dataclass
class BatchResult:
    results: list[PredictionResult | None]
    total_ms: float
    failed_count: int


class BatchPredictor:
    def __init__(self, predictor, max_batch_size: int = 32) -> None:
        self._predictor = predictor
        self._max_batch_size = max_batch_size

    async def predict_batch(self, texts: list[str], metadata: list[dict] | None = None) -> BatchResult:
        metadata = metadata or [{}] * len(texts)
        start = time.monotonic()

        results: list[PredictionResult | None] = [None] * len(texts)
        failed = 0

        for chunk_start in range(0, len(texts), self._max_batch_size):
            chunk_end = chunk_start + self._max_batch_size
            chunk_texts = texts[chunk_start:chunk_end]
            chunk_meta = metadata[chunk_start:chunk_end]

            tasks = [self._predictor.predict(text, meta) for text, meta in zip(chunk_texts, chunk_meta)]
            chunk_results = await asyncio.gather(*tasks, return_exceptions=True)

            for i, result in enumerate(chunk_results):
                global_idx = chunk_start + i
                if isinstance(result, Exception):
                    logger.warning("Batch prediction item failed", extra={"index": global_idx}, exc_info=result)
                    failed += 1
                else:
                    results[global_idx] = result

        return BatchResult(
            results=results,
            total_ms=(time.monotonic() - start) * 1000,
            failed_count=failed,
        )
