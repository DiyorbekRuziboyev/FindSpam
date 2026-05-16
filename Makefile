.PHONY: help dev build lint test clean setup migrate seed docker-up docker-down docker-logs

# ─── Meta ─────────────────────────────────────────────────────────────────────
help:
	@echo "FindSpam — Enterprise AI Spam Detection Platform"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Development:"
	@echo "  setup          Install all dependencies"
	@echo "  dev            Start all services in development mode"
	@echo "  dev-web        Start frontend only"
	@echo "  dev-api        Start backend API only"
	@echo "  dev-bot        Start Telegram bot only"
	@echo ""
	@echo "Quality:"
	@echo "  lint           Run all linters"
	@echo "  lint-fix       Run linters with auto-fix"
	@echo "  type-check     Run TypeScript type checking"
	@echo "  format         Format all code"
	@echo "  test           Run all tests"
	@echo "  test-api       Run API tests"
	@echo "  test-web       Run frontend tests"
	@echo ""
	@echo "Database:"
	@echo "  migrate        Run database migrations"
	@echo "  migrate-new    Create new migration"
	@echo "  seed           Seed development data"
	@echo ""
	@echo "Docker:"
	@echo "  docker-up      Start all Docker services"
	@echo "  docker-down    Stop all Docker services"
	@echo "  docker-logs    Tail all service logs"
	@echo "  docker-build   Rebuild all Docker images"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean          Remove all build artifacts"

# ─── Setup ────────────────────────────────────────────────────────────────────
setup:
	pnpm install
	cd apps/api && pip install -e ".[dev]"
	cd apps/ai-engine && pip install -e ".[dev]"
	cd apps/telegram-bot && pip install -e ".[dev]"
	@echo "Setup complete."

# ─── Development ──────────────────────────────────────────────────────────────
dev:
	turbo run dev

dev-web:
	pnpm --filter @findspam/web dev

dev-api:
	cd apps/api && uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-bot:
	cd apps/telegram-bot && python main.py

dev-ai:
	cd apps/ai-engine && python main.py

# ─── Quality ──────────────────────────────────────────────────────────────────
lint:
	turbo run lint
	cd apps/api && ruff check .
	cd apps/ai-engine && ruff check .
	cd apps/telegram-bot && ruff check .

lint-fix:
	turbo run lint:fix
	cd apps/api && ruff check --fix .
	cd apps/ai-engine && ruff check --fix .
	cd apps/telegram-bot && ruff check --fix .

type-check:
	turbo run type-check
	cd apps/api && mypy .
	cd apps/ai-engine && mypy .
	cd apps/telegram-bot && mypy .

format:
	pnpm run format
	cd apps/api && ruff format .
	cd apps/ai-engine && ruff format .
	cd apps/telegram-bot && ruff format .

test:
	turbo run test
	cd apps/api && pytest
	cd apps/ai-engine && pytest
	cd apps/telegram-bot && pytest

test-api:
	cd apps/api && pytest --cov=. --cov-report=html

test-web:
	pnpm --filter @findspam/web test

# ─── Database ─────────────────────────────────────────────────────────────────
migrate:
	cd apps/api && alembic upgrade head

migrate-new:
	cd apps/api && alembic revision --autogenerate -m "$(name)"

seed:
	cd apps/api && python -m scripts.seed

# ─── Docker ───────────────────────────────────────────────────────────────────
docker-up:
	docker compose -f infrastructure/compose/docker-compose.yml up -d

docker-up-dev:
	docker compose -f infrastructure/compose/docker-compose.yml \
		-f infrastructure/compose/docker-compose.dev.yml up -d

docker-down:
	docker compose -f infrastructure/compose/docker-compose.yml down

docker-logs:
	docker compose -f infrastructure/compose/docker-compose.yml logs -f

docker-build:
	docker compose -f infrastructure/compose/docker-compose.yml build

# ─── Maintenance ──────────────────────────────────────────────────────────────
clean:
	turbo run clean
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
