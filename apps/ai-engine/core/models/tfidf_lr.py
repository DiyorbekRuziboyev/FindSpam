import asyncio
import logging
from pathlib import Path

from core.models.base import BaseModelAdapter, ModelPrediction

logger = logging.getLogger(__name__)

_ARTIFACTS_DIR = Path(__file__).parents[3] / "model_artifacts"
_PIPELINE_PATH = _ARTIFACTS_DIR / "tfidf_lr_pipeline.joblib"

_LABEL_MAP = {0: "ham", 1: "spam"}
_CATEGORIES = ["SCAM", "PHISHING", "ADVERTISEMENT", "FAKE_GIVEAWAY", "SOCIAL_ENGINEERING", "SUSPICIOUS_URL", "OTHER"]


class TFIDFLogisticRegressionAdapter(BaseModelAdapter):
    def __init__(self) -> None:
        self._pipeline = None

    @property
    def name(self) -> str:
        return "tfidf_lr"

    def load(self) -> None:
        if not _PIPELINE_PATH.exists():
            logger.warning(
                "TF-IDF+LR pipeline artifact not found; adapter will return stub predictions",
                extra={"path": str(_PIPELINE_PATH)},
            )
            return

        try:
            import joblib

            self._pipeline = joblib.load(_PIPELINE_PATH)
            self._is_loaded = True
            logger.info("TF-IDF+LR pipeline loaded", extra={"path": str(_PIPELINE_PATH)})
        except Exception:
            logger.exception("Failed to load TF-IDF+LR pipeline")

    def _sync_predict(self, text: str) -> ModelPrediction:
        proba = self._pipeline.predict_proba([text])[0]
        spam_probability = float(proba[1]) if len(proba) > 1 else float(proba[0])
        category_scores = {cat: spam_probability / len(_CATEGORIES) for cat in _CATEGORIES}

        return ModelPrediction(
            spam_probability=spam_probability,
            category_scores=category_scores,
            is_loaded=True,
            model_name=self.name,
            raw_logits=proba.tolist(),
        )

    async def predict(self, text: str) -> ModelPrediction:
        if not self._is_loaded or self._pipeline is None:
            return self.stub_prediction()
        return await asyncio.to_thread(self._sync_predict, text)

    def _sync_predict_batch(self, texts: list[str]) -> list[ModelPrediction]:
        probas = self._pipeline.predict_proba(texts)
        results = []
        for proba in probas:
            spam_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])
            category_scores = {cat: spam_prob / len(_CATEGORIES) for cat in _CATEGORIES}
            results.append(
                ModelPrediction(
                    spam_probability=spam_prob,
                    category_scores=category_scores,
                    is_loaded=True,
                    model_name=self.name,
                    raw_logits=proba.tolist(),
                )
            )
        return results

    async def predict_batch(self, texts: list[str]) -> list[ModelPrediction]:
        if not self._is_loaded or self._pipeline is None:
            return [self.stub_prediction() for _ in texts]
        return await asyncio.to_thread(self._sync_predict_batch, texts)

    def train(self, texts: list[str], labels: list[int]) -> None:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        import joblib

        self._pipeline = Pipeline(
            [
                ("tfidf", TfidfVectorizer(max_features=10000, ngram_range=(1, 2), sublinear_tf=True)),
                ("lr", LogisticRegression(max_iter=1000, C=1.0, class_weight="balanced")),
            ]
        )
        self._pipeline.fit(texts, labels)
        self._is_loaded = True

        _ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(self._pipeline, _PIPELINE_PATH)
        logger.info("TF-IDF+LR pipeline trained and saved", extra={"samples": len(texts), "path": str(_PIPELINE_PATH)})
