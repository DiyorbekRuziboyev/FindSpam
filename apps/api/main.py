from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config.settings import get_settings
from core.logging.setup import configure_logging

settings = get_settings()


def create_app() -> FastAPI:
    configure_logging(settings.log_level)

    app = FastAPI(
        title="FindSpam API",
        description="Enterprise AI-powered spam detection platform API",
        version="1.0.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
    )

    _register_middleware(app)
    _register_routers(app)
    _register_exception_handlers(app)

    return app


def _register_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _register_routers(app: FastAPI) -> None:
    from modules.auth.presentation.router import router as auth_router
    from modules.moderation.presentation.router import router as moderation_router
    from modules.ai.presentation.router import router as ai_router
    from modules.analytics.presentation.router import router as analytics_router
    from modules.users.presentation.router import router as users_router
    from modules.telegram.presentation.router import router as telegram_router
    from modules.blacklist.presentation.router import router as blacklist_router
    from modules.audit.presentation.router import router as audit_router

    prefix = settings.api_prefix

    app.include_router(auth_router, prefix=f"{prefix}/auth", tags=["Auth"])
    app.include_router(moderation_router, prefix=f"{prefix}/moderation", tags=["Moderation"])
    app.include_router(ai_router, prefix=f"{prefix}/ai", tags=["AI Engine"])
    app.include_router(analytics_router, prefix=f"{prefix}/analytics", tags=["Analytics"])
    app.include_router(users_router, prefix=f"{prefix}/users", tags=["Users"])
    app.include_router(telegram_router, prefix=f"{prefix}/telegram", tags=["Telegram"])
    app.include_router(blacklist_router, prefix=f"{prefix}/blacklist", tags=["Blacklist"])
    app.include_router(audit_router, prefix=f"{prefix}/audit", tags=["Audit"])


def _register_exception_handlers(app: FastAPI) -> None:
    from core.exceptions.handlers import register_handlers

    register_handlers(app)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "healthy", "service": "findspam-api"}


app = create_app()
