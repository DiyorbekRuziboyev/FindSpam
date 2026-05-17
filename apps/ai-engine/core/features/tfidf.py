import asyncio
import logging
from pathlib import Path

import numpy as np

from core.features.base import BaseFeatureExtractor, FeatureVector

logger = logging.getLogger(__name__)

_ARTIFACTS_DIR = Path(__file__).parents[3] / "model_artifacts"
_VECTORIZER_PATH = _ARTIFACTS_DIR / "tfidf_vectorizer.joblib"


class TFIDFFeatureExtractor(BaseFeatureExtractor):
    def __init__(self) -> None:
        self._vectorizer = None
        self._feature_names_list: list[str] = []

    @property
    def name(self) -> str:
        return "tfidf"

    def fit(self, texts: list[str]) -> None:
        from sklearn.feature_extraction.text import TfidfVectorizer
        import joblib

        self._vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=2,
        )
        self._vectorizer.fit(texts)
        self._feature_names_list = self._vectorizer.get_feature_names_out().tolist()

        _ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(self._vectorizer, _VECTORIZER_PATH)
        logger.info("TF-IDF vectorizer fitted and saved", extra={"path": str(_VECTORIZER_PATH)})

    def _load(self) -> None:
        if self._vectorizer is not None:
            return
        if not _VECTORIZER_PATH.exists():
            logger.warning("TF-IDF vectorizer artifact not found; extractor will return zeros", extra={"path": str(_VECTORIZER_PATH)})
            return
        import joblib

        self._vectorizer = joblib.load(_VECTORIZER_PATH)
        self._feature_names_list = self._vectorizer.get_feature_names_out().tolist()
        logger.info("TF-IDF vectorizer loaded", extra={"features": len(self._feature_names_list)})

    def _sync_transform(self, text: str) -> np.ndarray:
        self._load()
        if self._vectorizer is None:
            return np.zeros(0, dtype=np.float32)
        result = self._vectorizer.transform([text])
        return result.toarray()[0].astype(np.float32)

    def extract(self, text: str, **context: object) -> FeatureVector:
        self._load()
        if self._vectorizer is None:
            return FeatureVector(name=self.name, features=np.zeros(0, dtype=np.float32), feature_names=[])

        result = self._vectorizer.transform([text])
        features = result.toarray()[0].astype(np.float32)
        return FeatureVector(name=self.name, features=features, feature_names=self._feature_names_list)

    async def extract_async(self, text: str, **context: object) -> FeatureVector:
        return await asyncio.to_thread(self.extract, text, **context)
