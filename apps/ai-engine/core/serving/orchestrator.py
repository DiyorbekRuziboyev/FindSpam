from __future__ import annotations

import asyncio
import hashlib
import logging
import time

from core.config import get_ai_settings
from core.ensemble.weighted import WeightedAverageEnsemble
from core.explainability.shap_explainer import SHAPExplainer
from core.models.base import ModelPrediction
from core.models.registry import ModelRegistry
from core.preprocessor.pipeline import PreprocessingPipeline
from core.serving.predictor import ModelContributions, PredictionResult, SpamCategory, ThreatLevel

logger = logging.getLogger(__name__)

_CATEGORY_TO_API_MAP: dict[str, str] = {
    "ADVERTISEMENT": "MALICIOUS_AD",
}


def _to_api_category(category: str | None) -> SpamCategory | None:
    if category is None:
        return None
    mapped = _CATEGORY_TO_API_MAP.get(category, category)
    try:
        return SpamCategory(mapped)
    except ValueError:
        logger.warning("Unknown spam category; defaulting to OTHER", extra={"category": category})
        return SpamCategory.OTHER


def _score_to_threat_level(score: float, threshold_spam: float, threshold_suspicious: float, threshold_review: float) -> ThreatLevel:
    if score >= threshold_spam:
        return ThreatLevel.CRITICAL if score >= 0.95 else ThreatLevel.HIGH
    if score >= threshold_suspicious:
        return ThreatLevel.MEDIUM
    if score >= threshold_review:
        return ThreatLevel.LOW
    return ThreatLevel.NONE


def _cache_key(text: str, model_version: str) -> str:
    text_hash = hashlib.sha256(text.encode()).hexdigest()
    return f"pred:{model_version}:{text_hash}"


def _result_to_dict(result: PredictionResult) -> dict:
    return {
        "is_spam": result.is_spam,
        "confidence": result.confidence,
        "threat_level": result.threat_level,
        "spam_category": result.spam_category,
        "model_contributions": {
            "xlm_roberta": result.model_contributions.xlm_roberta,
            "mbert": result.model_contributions.mbert,
            "tfidf_lr": result.model_contributions.tfidf_lr,
            "rule_engine": result.model_contributions.rule_engine,
        },
        "explanation": result.explanation,
        "processing_ms": result.processing_ms,
    }


def _dict_to_result(data: dict) -> PredictionResult:
    mc = data["model_contributions"]
    cat = data.get("spam_category")
    return PredictionResult(
        is_spam=data["is_spam"],
        confidence=data["confidence"],
        threat_level=ThreatLevel(data["threat_level"]),
        spam_category=SpamCategory(cat) if cat else None,
        model_contributions=ModelContributions(
            xlm_roberta=mc["xlm_roberta"],
            mbert=mc["mbert"],
            tfidf_lr=mc["tfidf_lr"],
            rule_engine=mc["rule_engine"],
        ),
        explanation=data["explanation"],
        processing_ms=data["processing_ms"],
    )


class EnsemblePredictor:
    def __init__(
        self,
        model_registry: ModelRegistry,
        cache=None,
    ) -> None:
        self._registry = model_registry
        self._cache = cache
        self._preprocessor = PreprocessingPipeline()
        self._ensemble = WeightedAverageEnsemble()
        self._explainer: SHAPExplainer | None = None

        settings = get_ai_settings()
        self._weights = {
            "xlm_roberta": settings.weight_xlm_roberta,
            "mbert": settings.weight_mbert,
            "tfidf_lr": settings.weight_tfidf_lr,
            "rule_engine": settings.weight_rule_engine,
        }
        self._threshold_spam = settings.threshold_spam
        self._threshold_suspicious = settings.threshold_suspicious
        self._threshold_review = settings.threshold_review
        self._model_version = f"{settings.xlm_roberta_model}:{settings.mbert_model}"

    def set_explainer(self, explainer: SHAPExplainer) -> None:
        self._explainer = explainer

    async def _run_models(self, text: str) -> dict[str, ModelPrediction]:
        adapters = self._registry.all()
        tasks = [adapter.predict(text) for adapter in adapters]
        results_list = await asyncio.gather(*tasks, return_exceptions=True)

        predictions: dict[str, ModelPrediction] = {}
        for adapter, result in zip(adapters, results_list):
            if isinstance(result, Exception):
                logger.warning("Model prediction raised", extra={"model": adapter.name}, exc_info=result)
                predictions[adapter.name] = adapter.stub_prediction()
            else:
                predictions[adapter.name] = result

        return predictions

    async def predict(self, text: str, metadata: dict | None = None) -> PredictionResult:
        metadata = metadata or {}
        start = time.monotonic()

        cache_key = _cache_key(text, self._model_version)
        if self._cache:
            cached = await self._cache.get(cache_key)
            if cached:
                return _dict_to_result(cached)

        processed = await self._preprocessor.process(text)
        predictions = await self._run_models(processed.normalized)

        ensemble_result = self._ensemble.combine(predictions, self._weights)
        spam_score = ensemble_result.final_score

        threat_level = _score_to_threat_level(
            spam_score, self._threshold_spam, self._threshold_suspicious, self._threshold_review
        )
        is_spam = spam_score >= self._threshold_spam
        api_category = _to_api_category(ensemble_result.category)

        contributions = ModelContributions(
            xlm_roberta=ensemble_result.contributions.get("xlm_roberta", 0.0),
            mbert=ensemble_result.contributions.get("mbert", 0.0),
            tfidf_lr=ensemble_result.contributions.get("tfidf_lr", 0.0),
            rule_engine=ensemble_result.contributions.get("rule_engine", 0.0),
        )

        if self._explainer:
            explanation_obj = await self._explainer.explain_async(
                text,
                ensemble_result.contributions,
                spam_score,
                ensemble_result.category,
            )
            explanation = {
                "summary": explanation_obj.summary,
                "triggered_rules": explanation_obj.triggered_rules,
                "top_tokens": [{"token": t.token, "importance": t.importance} for t in explanation_obj.top_tokens],
            }
        else:
            explanation = {"summary": "Explainability not configured.", "triggered_rules": [], "top_tokens": []}

        result = PredictionResult(
            is_spam=is_spam,
            confidence=spam_score,
            threat_level=threat_level,
            spam_category=api_category,
            model_contributions=contributions,
            explanation=explanation,
            processing_ms=(time.monotonic() - start) * 1000,
        )

        if self._cache:
            await self._cache.set(cache_key, _result_to_dict(result))

        return result

    async def predict_batch(self, texts: list[str], metadata: list[dict] | None = None) -> list[PredictionResult]:
        metadata = metadata or [{}] * len(texts)
        tasks = [self.predict(text, meta) for text, meta in zip(texts, metadata)]
        return list(await asyncio.gather(*tasks))
