import uvicorn
from fastapi import FastAPI

from core.config import get_ai_settings

settings = get_ai_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title="FindSpam AI Engine",
        description="Hybrid ensemble AI inference service",
        version="1.0.0",
        docs_url="/docs" if settings.debug else None,
    )

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "healthy", "service": "findspam-ai-engine"}

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
