FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TRANSFORMERS_CACHE=/app/model_artifacts/.cache

WORKDIR /app

FROM base AS deps
COPY pyproject.toml ./
RUN pip install hatchling && pip install -e .

FROM deps AS production
COPY . .
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

RUN mkdir -p /app/model_artifacts && chown -R appuser:appgroup /app/model_artifacts
USER appuser

VOLUME ["/app/model_artifacts"]
EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "1"]

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1
