from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import router
from core.config import get_ai_settings
from core.explainability.shap_explainer import SHAPExplainer
from core.models.registry import ModelRegistry
from core.serving.cache import InferenceCache
from core.serving.orchestrator import EnsemblePredictor
from core.training.feedback_collector import FeedbackCollector
from monitoring.audit import PredictionAuditor
from monitoring.metrics import InferenceMetrics

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = logging.getLogger(__name__)
settings = get_ai_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("FindSpam AI Engine starting up")

    registry = ModelRegistry.default()
    load_results = registry.load_all()
    logger.info("Model loading complete", extra={"results": load_results})

    cache: InferenceCache | None = None
    try:
        import redis.asyncio as aioredis

        redis_client = aioredis.from_url(settings.redis_url, decode_responses=True)
        await redis_client.ping()
        cache = InferenceCache(redis_client, ttl=settings.prediction_cache_ttl)
        logger.info("Redis cache connected", extra={"url": settings.redis_url})
    except Exception:
        logger.warning("Redis unavailable; inference cache disabled — predictions will not be cached")

    predictor = EnsemblePredictor(model_registry=registry, cache=cache)

    tfidf_adapter = registry.get("tfidf_lr") if "tfidf_lr" in {a.name for a in registry.all()} else None
    tfidf_pipeline = getattr(tfidf_adapter, "_pipeline", None) if tfidf_adapter else None
    explainer = SHAPExplainer(tfidf_lr_pipeline=tfidf_pipeline)
    predictor.set_explainer(explainer)

    feedback_collector = FeedbackCollector()
    metrics = InferenceMetrics(window_size=1000)
    auditor = PredictionAuditor()

    app.state.predictor = predictor
    app.state.model_registry = registry
    app.state.feedback_collector = feedback_collector
    app.state.metrics = metrics
    app.state.auditor = auditor

    logger.info("FindSpam AI Engine ready")
    yield

    logger.info("FindSpam AI Engine shutting down")
    if cache:
        try:
            await redis_client.aclose()
        except Exception:
            pass


def create_app() -> FastAPI:
    app = FastAPI(
        title="FindSpam AI Engine",
        description="Hybrid ensemble AI inference service — XLM-RoBERTa + mBERT + TF-IDF + Rule Engine",
        version="1.0.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
