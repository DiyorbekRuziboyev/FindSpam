# FindSpam — Architecture Overview

## System Design

FindSpam is a **modular monolith** following **Clean Architecture** principles.
Each bounded context is a self-contained module with its own domain, application, infrastructure, and presentation layers.

## Bounded Contexts

| Module | Responsibility |
|---|---|
| `auth` | JWT authentication, refresh tokens, session management |
| `moderation` | Spam event lifecycle, action execution, review workflow |
| `ai` | Prediction requests, model management, feedback loop |
| `analytics` | Aggregated metrics, trend computation, dashboard stats |
| `users` | Platform admin user management and RBAC |
| `telegram` | Group registration, bot event ingestion, user tracking |
| `blacklist` | Domain/user blacklist and whitelist management |
| `notifications` | WebSocket broadcasting, alert routing |
| `audit` | Immutable audit trail for all state mutations |

## Communication Rules

- Cross-module calls: **Application service interfaces only** — never direct model imports
- Side effects: **In-process event bus** (`core/events/bus.py`)
- Realtime push: **Redis PubSub → WebSocket manager**

## Layer Responsibilities

```
Presentation   → FastAPI routes, WebSocket handlers, Pydantic schemas
Application    → Use cases, orchestration, DTO mapping
Domain         → Entities, value objects, domain services, domain events
Infrastructure → SQLAlchemy models, repositories, external API adapters
```

## Data Flow

```
Bot/Client → Nginx → FastAPI Router → Use Case
                                        ├── Repository → PostgreSQL
                                        ├── AI Adapter → AI Engine
                                        ├── Cache → Redis
                                        └── Event Bus → Handlers
                                                          ├── Audit logger
                                                          ├── Analytics recorder
                                                          └── WS broadcaster → Dashboard
```

## AI Pipeline

```
Text Input
  → Preprocessing (lang detect, normalize, tokenize)
  → Feature Extraction (semantic + statistical + behavioral)
  → Ensemble (XLM-RoBERTa + mBERT + TF-IDF/LR + Rules)
  → Confidence Scoring + Threshold Classification
  → Explainability (SHAP + LIME)
  → PredictionResult
```

See the [full architecture design](../../CLAUDE.md) for detailed diagrams.
