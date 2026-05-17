from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Request, status

from api.schemas import (
    BatchPredictRequest,
    BatchPredictResponse,
    FeedbackRequest,
    HealthResponse,
    ModelContributionsSchema,
    PredictRequest,
    PredictResponse,
)
from core.serving.batch import BatchPredictor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["AI Moderation"])


def _predictor(request: Request):
    predictor = getattr(request.app.state, "predictor", None)
    if predictor is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Predictor not initialized")
    return predictor


def _feedback_collector(request: Request):
    return getattr(request.app.state, "feedback_collector", None)


def _registry(request: Request):
    return getattr(request.app.state, "model_registry", None)


@router.post("/predict", response_model=PredictResponse)
async def predict(body: PredictRequest, request: Request) -> PredictResponse:
    predictor = _predictor(request)
    try:
        result = await predictor.predict(body.text, body.metadata)
    except Exception:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Prediction failed")

    return PredictResponse(
        is_spam=result.is_spam,
        confidence=result.confidence,
        threat_level=result.threat_level,
        spam_category=result.spam_category,
        model_contributions=ModelContributionsSchema(
            xlm_roberta=result.model_contributions.xlm_roberta,
            mbert=result.model_contributions.mbert,
            tfidf_lr=result.model_contributions.tfidf_lr,
            rule_engine=result.model_contributions.rule_engine,
        ),
        explanation=result.explanation,
        processing_ms=result.processing_ms,
    )


@router.post("/predict/batch", response_model=BatchPredictResponse)
async def predict_batch(body: BatchPredictRequest, request: Request) -> BatchPredictResponse:
    predictor = _predictor(request)
    batch = BatchPredictor(predictor)

    batch_result = await batch.predict_batch(body.texts, body.metadata)

    results = []
    for r in batch_result.results:
        if r is None:
            results.append(None)
        else:
            results.append(
                PredictResponse(
                    is_spam=r.is_spam,
                    confidence=r.confidence,
                    threat_level=r.threat_level,
                    spam_category=r.spam_category,
                    model_contributions=ModelContributionsSchema(
                        xlm_roberta=r.model_contributions.xlm_roberta,
                        mbert=r.model_contributions.mbert,
                        tfidf_lr=r.model_contributions.tfidf_lr,
                        rule_engine=r.model_contributions.rule_engine,
                    ),
                    explanation=r.explanation,
                    processing_ms=r.processing_ms,
                )
            )

    return BatchPredictResponse(
        results=results,
        total_ms=batch_result.total_ms,
        failed_count=batch_result.failed_count,
    )


@router.post("/feedback", status_code=status.HTTP_204_NO_CONTENT)
async def submit_feedback(body: FeedbackRequest, request: Request) -> None:
    collector = _feedback_collector(request)
    if collector is None:
        return
    collector.record(
        text=body.text,
        predicted_spam=body.predicted_spam,
        is_spam=body.is_spam,
        confidence=body.confidence,
        source=body.source,
    )


@router.get("/health", response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    registry = _registry(request)
    models_loaded: dict[str, bool] = {}
    if registry:
        for adapter in registry.all():
            models_loaded[adapter.name] = adapter.is_loaded

    return HealthResponse(
        status="healthy",
        service="findspam-ai-engine",
        models_loaded=models_loaded,
        version="1.0.0",
    )
