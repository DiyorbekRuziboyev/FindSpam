from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from sqlalchemy import text

from core.config.database import engine, get_db_session
from core.config.redis import get_redis_client
from core.config.settings import get_settings
from core.logging.setup import configure_logging
from core.middleware import (
    RateLimitMiddleware,
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
    TimingMiddleware,
)

settings = get_settings()
logger = structlog.get_logger(__name__)

_OPENAPI_TAGS = [
    {
        "name": "Auth",
        "description": "Authentication — JWT-based login, refresh, logout, and profile.",
    },
    {
        "name": "Users",
        "description": "Platform user management — CRUD and role assignment.",
    },
    {
        "name": "Moderation",
        "description": "Moderation events — review queue, decisions, and statistics.",
    },
    {
        "name": "AI Engine",
        "description": "AI prediction endpoints — inference, feedback, model versions, and metrics.",
    },
    {
        "name": "Analytics",
        "description": "Dashboard, trends, historical snapshots, and breakdowns.",
    },
    {
        "name": "Telegram",
        "description": "Telegram group and user management — bans, settings, stats.",
    },
    {
        "name": "Blacklist",
        "description": "Blacklist and whitelist management — domains, usernames, IPs, emails.",
    },
    {
        "name": "Audit",
        "description": "Immutable audit trail — all platform state mutations are logged here.",
    },
    {
        "name": "Notifications",
        "description": "Real-time WebSocket notification stream and channel registry.",
    },
    {
        "name": "Health",
        "description": "Liveness and readiness probes for container orchestration.",
    },
]


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging(settings.log_level)
    logger.info("findspam_api_starting", env=settings.app_env, version=settings.app_version)
    yield
    await engine.dispose()
    logger.info("findspam_api_stopped")


def _generate_operation_id(route: APIRoute) -> str:
    tag = route.tags[0] if route.tags else "root"
    return f"{tag}:{route.name}"


def create_app() -> FastAPI:
    app = FastAPI(
        title="FindSpam API",
        description=(
            "Enterprise AI-powered Telegram spam, scam, and phishing detection platform.\n\n"
            "**Authentication**: Bearer JWT (RS256).\n\n"
            "**Rate limiting**: 5 req/15 min on `/auth/login`; 100 req/min everywhere else."
        ),
        version=settings.app_version,
        contact={
            "name": "FindSpam Engineering",
            "email": "engineering@findspam.io",
        },
        license_info={
            "name": "Proprietary — All Rights Reserved",
        },
        openapi_tags=_OPENAPI_TAGS,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
        generate_unique_id_function=_generate_operation_id,
        lifespan=_lifespan,
    )

    _register_middleware(app)
    _register_routers(app)
    _register_exception_handlers(app)
    _register_health(app)

    return app


def _register_middleware(app: FastAPI) -> None:
    # Starlette processes middleware LIFO — last added runs first on ingress.
    # Desired order: CORS → RateLimit → SecurityHeaders → Timing → RequestID → route
    # Register in reverse:
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitMiddleware, redis=get_redis_client())
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _register_routers(app: FastAPI) -> None:
    from modules.ai.presentation.router import router as ai_router
    from modules.analytics.presentation.router import router as analytics_router
    from modules.audit.presentation.router import router as audit_router
    from modules.auth.presentation.router import router as auth_router
    from modules.blacklist.presentation.router import router as blacklist_router
    from modules.moderation.presentation.router import router as moderation_router
    from modules.notifications.presentation.router import router as notifications_router
    from modules.telegram.presentation.router import router as telegram_router
    from modules.users.presentation.router import router as users_router

    prefix = settings.api_prefix

    app.include_router(auth_router, prefix=f"{prefix}/auth", tags=["Auth"])
    app.include_router(users_router, prefix=f"{prefix}/users", tags=["Users"])
    app.include_router(moderation_router, prefix=f"{prefix}/moderation", tags=["Moderation"])
    app.include_router(ai_router, prefix=f"{prefix}/ai", tags=["AI Engine"])
    app.include_router(analytics_router, prefix=f"{prefix}/analytics", tags=["Analytics"])
    app.include_router(telegram_router, prefix=f"{prefix}/telegram", tags=["Telegram"])
    app.include_router(blacklist_router, prefix=f"{prefix}/blacklist", tags=["Blacklist"])
    app.include_router(audit_router, prefix=f"{prefix}/audit", tags=["Audit"])
    app.include_router(
        notifications_router, prefix=f"{prefix}/notifications", tags=["Notifications"]
    )


def _register_exception_handlers(app: FastAPI) -> None:
    from core.exceptions.handlers import register_handlers

    register_handlers(app)


def _register_health(app: FastAPI) -> None:
    @app.get("/health", tags=["Health"], summary="Liveness probe")
    async def health_check() -> dict[str, str]:
        return {
            "status": "healthy",
            "service": "findspam-api",
            "version": settings.app_version,
            "env": settings.app_env,
        }

    @app.get("/health/ready", tags=["Health"], summary="Readiness probe")
    async def readiness_check() -> dict[str, str]:
        checks: dict[str, str] = {}

        # Database ping
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            checks["database"] = "ok"
        except Exception:
            checks["database"] = "unavailable"

        # Redis ping
        try:
            redis = get_redis_client()
            await redis.ping()
            checks["redis"] = "ok"
        except Exception:
            checks["redis"] = "unavailable"

        overall = "ready" if all(v == "ok" for v in checks.values()) else "degraded"
        return {"status": overall, **checks}

    @app.get("/health/live", tags=["Health"], summary="Kubernetes liveness probe")
    async def liveness_check() -> dict[str, str]:
        return {"status": "alive"}


app = create_app()
