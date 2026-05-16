# FindSpam API

Enterprise-grade FastAPI backend for the FindSpam AI-powered Telegram spam detection platform.

## Stack

| Layer | Technology |
|---|---|
| Runtime | Python 3.12 |
| Framework | FastAPI 0.115+ |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL (asyncpg) |
| Cache / Rate limit | Redis 7+ |
| Auth | JWT RS256 — python-jose |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Logging | structlog (JSON) |
| Serialisation | orjson |

## Architecture

```
apps/api/
├── core/                     # Cross-cutting infrastructure
│   ├── config/               # Settings, DB engine, Redis pool
│   ├── db/                   # Base, mixins, enums
│   ├── exceptions/           # Domain errors + exception handlers
│   ├── filters/              # BaseFilter, SortOrder
│   ├── logging/              # structlog JSON config
│   ├── middleware/           # RequestID, Timing, SecurityHeaders, RateLimit
│   ├── pagination/           # PaginationParams dependency
│   ├── realtime/             # WebSocketManager (room-based broadcast)
│   ├── repository/           # Abstract + SQLAlchemy base repository
│   ├── schemas/              # StandardResponse[T], PaginatedResponse[T]
│   ├── security/             # JWT, bcrypt, RBAC, auth dependencies
│   └── services/             # BaseService
│
├── modules/                  # Feature modules (modular monolith)
│   ├── auth/                 # Login, logout, refresh, /me
│   ├── users/                # Platform user management
│   ├── moderation/           # Moderation events and review queue
│   ├── ai/                   # AI predictions, feedback, model versions
│   ├── analytics/            # Dashboard, trends, snapshots
│   ├── telegram/             # Group and user management
│   ├── blacklist/            # Blacklist / whitelist management
│   ├── audit/                # Immutable audit log
│   └── notifications/        # Real-time WebSocket stream
│
├── migrations/               # Alembic migration files
│   └── versions/
│       └── 001_initial_schema.py
│
├── main.py                   # FastAPI app factory
└── pyproject.toml
```

Each module follows Clean Architecture layers:

```
modules/<name>/
├── domain/          # Entities, value objects, domain events
├── application/     # Use cases, DTOs, commands
├── infrastructure/  # SQLAlchemy models, repositories
└── presentation/    # FastAPI router, Pydantic schemas
```

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 16+
- Redis 7+
- RSA key pair for JWT (see [Key Generation](#key-generation))

### Setup

```bash
cd apps/api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Copy and configure environment
cp ../../.env.example ../../.env
# Edit .env with your DATABASE_URL, REDIS_URL, TELEGRAM_BOT_TOKEN

# Run migrations
alembic upgrade head

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Key Generation

JWT uses RS256. Generate a key pair once and reference via `.env`:

```bash
mkdir -p infrastructure/keys
openssl genrsa -out infrastructure/keys/private.pem 4096
openssl rsa -in infrastructure/keys/private.pem -pubout -out infrastructure/keys/public.pem
```

Set in `.env`:
```
JWT_PRIVATE_KEY_PATH=./infrastructure/keys/private.pem
JWT_PUBLIC_KEY_PATH=./infrastructure/keys/public.pem
```

## API

| Base URL | `/api/v1` |
|---|---|
| Docs (debug only) | `GET /docs` |
| OpenAPI schema | `GET /openapi.json` |
| Liveness | `GET /health/live` |
| Readiness | `GET /health/ready` |

### Authentication

All protected endpoints require:

```
Authorization: Bearer <access_token>
```

Access tokens expire in **15 minutes**. Use `POST /api/v1/auth/refresh` with a valid refresh token to rotate them. Refresh tokens expire in **30 days** and are rotated on every use (token family invalidation on reuse detection).

### Rate Limiting

| Endpoint | Limit |
|---|---|
| `POST /api/v1/auth/login` | 5 requests / 15 minutes per IP |
| All other endpoints | 100 requests / minute per IP |

Exceeding limits returns `HTTP 429` with a `Retry-After` header.

### RBAC Roles

| Role | Description |
|---|---|
| `SUPER_ADMIN` | Full platform access |
| `ADMIN` | User management, all operational features |
| `ANALYST` | Read-only analytics and AI metrics |
| `MODERATOR` | Review queue and Telegram moderation actions |

## Modules

| Module | Prefix | Description |
|---|---|---|
| auth | `/api/v1/auth` | Login, logout, refresh, profile |
| users | `/api/v1/users` | Platform user CRUD |
| moderation | `/api/v1/moderation` | Moderation events and review queue |
| ai | `/api/v1/ai` | AI inference, feedback, model management |
| analytics | `/api/v1/analytics` | Dashboard, trends, breakdowns |
| telegram | `/api/v1/telegram` | Group and user management |
| blacklist | `/api/v1/blacklist` | Blacklist/whitelist management |
| audit | `/api/v1/audit` | Immutable audit trail |
| notifications | `/api/v1/notifications` | Real-time WebSocket stream |

## Response Envelope

All endpoints return a consistent JSON envelope:

**Success (single item)**
```json
{ "success": true, "data": { ... }, "message": null }
```

**Success (paginated list)**
```json
{
  "success": true,
  "data": [ ... ],
  "meta": {
    "page": 1, "page_size": 20, "total_items": 100,
    "total_pages": 5, "has_next": true, "has_prev": false
  }
}
```

**Error**
```json
{
  "success": false,
  "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [ ... ] }
}
```

## Development

### Linting and Formatting

```bash
# Check
ruff check apps/api/

# Format
ruff format apps/api/

# Type-check
mypy apps/api/ --config-file apps/api/pyproject.toml
```

### Pre-commit Hooks

```bash
# Install hooks (run once from repo root)
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

### Testing

```bash
cd apps/api
pytest --cov=. --cov-report=term-missing
```

## Security

- Passwords: bcrypt (rounds=12), never logged or returned
- Refresh tokens: SHA256-hashed in DB, raw token only returned once
- JWT: RS256 with file-based key pair
- Rate limiting: Redis sliding-window per IP
- Security headers: HSTS, CSP, X-Frame-Options, X-Content-Type-Options
- SQL injection: SQLAlchemy ORM only — no raw SQL
- Audit logging: all state mutations logged to `audit_logs`
- Token theft detection: refresh token family invalidation on reuse
