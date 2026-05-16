# FindSpam

Enterprise AI-powered spam and scam detection platform for Uzbek-speaking communities.

## Overview

FindSpam is a production-grade AI moderation ecosystem that combines transformer-based NLP, ensemble machine learning, and real-time Telegram moderation to protect communities from spam, scams, phishing, and social engineering.

**Supported languages:** Uzbek (Latin & Cyrillic), Russian, English

## Architecture

```
findspam/
├── apps/
│   ├── web/              # Next.js 15 admin dashboard
│   ├── api/              # FastAPI backend (modular monolith)
│   ├── ai-engine/        # Hybrid AI inference & training
│   └── telegram-bot/     # aiogram 3 moderation bot
├── packages/
│   ├── ui/               # Shared UI component library
│   ├── config/           # Shared ESLint, TypeScript, Tailwind configs
│   ├── types/            # Shared TypeScript type definitions
│   └── utils/            # Shared utilities
├── infrastructure/       # Docker, Nginx, compose configs
├── docs/                 # Architecture and API documentation
└── datasets/             # Training data (gitignored raw/processed)
```

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, TailwindCSS, shadcn/ui, Framer Motion |
| State | Zustand, TanStack Query |
| Backend | FastAPI, Python 3.12, SQLAlchemy 2.0, Alembic, Pydantic v2 |
| Database | PostgreSQL 16, Redis 7 |
| AI | XLM-RoBERTa, mBERT, TF-IDF + LR, SHAP, scikit-learn |
| Bot | aiogram 3 |
| DevOps | Docker, Docker Compose, Nginx |

## Getting Started

### Prerequisites

- Node.js >= 20, pnpm >= 9
- Python 3.12
- Docker & Docker Compose

### Setup

```bash
cp .env.example .env
make setup
make docker-up
make migrate
make dev
```

### Services

| Service | URL |
|---|---|
| Admin Dashboard | http://localhost:3000 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| AI Engine | http://localhost:8001 |

## Development

```bash
make dev          # Start all services
make test         # Run all tests
make lint         # Lint all code
make migrate      # Run DB migrations
```

## Documentation

See [`docs/architecture/`](docs/architecture/) for full system architecture.
