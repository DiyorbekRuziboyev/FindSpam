# FindSpam Telegram Bot

Enterprise-grade Telegram moderation bot for real-time spam, scam, and phishing detection.

---

## Architecture

```
telegram-bot/
├── core/
│   ├── config.py          # BotSettings (pydantic-settings)
│   ├── api_client.py      # FindSpamAPIClient — httpx, no module-level singleton
│   ├── event_bus.py       # Redis pub/sub publisher for admin dashboard
│   └── setup.py           # Dispatcher factory with dependency injection
├── handlers/
│   ├── commands/
│   │   ├── start.py       # /start, /help
│   │   ├── moderation.py  # /warn, /mute, /unmute, /ban, /unban, /kick
│   │   ├── settings.py    # /settings — group configuration wizard
│   │   └── stats.py       # /stats — group moderation statistics
│   ├── messages/
│   │   └── text.py        # Text/caption handler: flood check → AI prediction → action
│   ├── callbacks/
│   │   └── moderation.py  # Inline keyboard callbacks: mod:* and settings:*
│   └── events/
│       └── new_member.py  # Anti-raid detection on chat_member updates
├── middlewares/
│   ├── logging.py         # Outer: structured JSON logging via structlog
│   ├── rate_limiter.py    # Outer: Redis INCR per-user rate limiter
│   └── spam_detector.py   # Inner: AI engine call, injects spam_prediction
├── services/
│   ├── flood_detector.py  # Redis flood:{chat_id}:{user_id} counter
│   ├── anti_raid.py       # Redis raid:{chat_id}:joins counter
│   ├── moderation_service.py # warn, mute, temp_ban, permanent_ban, unban, kick
│   ├── group_service.py   # Group settings with Redis cache + backend API
│   └── audit_service.py   # Structured audit records → backend API + event bus
├── filters/
│   ├── admin.py           # IsAdmin, IsSuperAdmin
│   ├── chat.py            # IsGroupMessage
│   └── user.py            # NotBot, IsNotMuted
├── keyboards/
│   └── inline/
│       ├── moderation.py  # moderation_action_keyboard, whitelist_keyboard
│       └── settings.py    # settings_menu_keyboard, language_keyboard, confirm_keyboard
├── states/
│   └── settings.py        # GroupSettingsForm FSM states
├── locales/
│   ├── uz_lat.py          # Uzbek Latin message strings
│   ├── uz_cyr.py          # Uzbek Cyrillic message strings
│   ├── ru.py              # Russian message strings
│   └── en.py              # English message strings
└── main.py                # Async entrypoint: lifespan, polling/webhook
```

---

## Key Design Decisions

### Dependency Injection via workflow_data

All shared resources are stored in `dp["key"]` during startup and received by handlers
via `data["key"]`. No module-level singletons. This enables:
- Clean lifecycle management (open in startup, close in shutdown)
- Testability (swap mocks in tests)
- No `httpx.AsyncClient` created before the event loop starts

```python
dp["redis"] = redis
dp["api_client"] = api_client
dp["settings"] = settings
```

### Middleware Stack

```
Message arrives
    → LoggingMiddleware (outer) — timing + structured log
    → RateLimiterMiddleware (outer) — Redis INCR+EXPIRE per user, drop if over limit
    → SpamDetectorMiddleware (inner) — AI engine call, inject spam_prediction
    → Handler
```

### Flood Detection (fast path before AI)

```python
key = f"flood:{chat_id}:{user_id}"
count = await redis.incr(key)
if count == 1: await redis.expire(key, window=60)
if count > threshold(5): auto_mute(duration=300s)
```

The flood check runs in the message handler **before** the AI prediction is read.
Prevents abuse and saves AI inference calls.

### Anti-Raid Detection

```python
key = f"raid:{chat_id}:joins"
count = await redis.incr(key)
if count == 1: await redis.expire(key, window=30)
if count > threshold(10): alert_admins()
```

Triggered from `chat_member` updates on every new member join.

### Event Bus (Real-Time Dashboard Integration)

Every moderation action is published to `findspam:moderation_events` Redis pub/sub channel.
The admin dashboard subscribes and receives live events for monitoring.

```python
await event_bus.publish_spam_detected(
    chat_id=..., user_id=..., message_id=...,
    confidence=0.93, threat_level="HIGH", spam_category="PHISHING",
    action_taken="DELETE",
)
```

---

## Spam Detection Flow

```
Text message received
    → Rate limit check (Redis) → drop if exceeded
    → SpamDetectorMiddleware → POST /ai/predict → spam_prediction injected
    → Text handler:
        1. Flood check (Redis fast path)
        2. Read spam_prediction confidence + threat_level
        3. CRITICAL/HIGH + above threshold → delete + warn + notify admins
        4. MEDIUM/LOW + above suspicious threshold → flag for admin review
        5. NONE → pass through
```

---

## Supported Languages

| Code | Language |
|---|---|
| `uz_lat` | Uzbek Latin |
| `uz_cyr` | Uzbek Cyrillic |
| `ru` | Russian |
| `en` | English |

Language is configured per-group via `/settings` and persisted to the backend API.

---

## Configuration

All settings via environment variables (`.env` file):

```env
TELEGRAM_BOT_TOKEN=your_bot_token

# Webhook (optional, polling by default)
USE_WEBHOOK=false
WEBHOOK_URL=https://your-domain.com/webhook
WEBHOOK_PATH=/webhook
WEBHOOK_SECRET=your_secret
WEBHOOK_PORT=8080

# Backend API
API_BASE_URL=http://localhost:8000/api/v1
API_SERVICE_TOKEN=your_service_token

# Redis
REDIS_URL=redis://localhost:6379/1

# Moderation thresholds
SPAM_CONFIDENCE_THRESHOLD=0.80
SUSPICIOUS_THRESHOLD=0.60

# Rate limiting
RATE_LIMIT_MESSAGES=20
RATE_LIMIT_WINDOW=60

# Flood detection
FLOOD_THRESHOLD=5
FLOOD_WINDOW=60
FLOOD_MUTE_DURATION=300

# Anti-raid
RAID_JOIN_THRESHOLD=10
RAID_WINDOW=30
```

---

## Admin Commands

All moderation commands require admin privileges in the group.

| Command | Description |
|---|---|
| `/warn` | Warn a user (reply to their message) |
| `/mute` | Mute a user for 10 minutes |
| `/unmute` | Remove mute restriction |
| `/ban` | Permanently ban a user |
| `/unban` | Unban a user |
| `/kick` | Kick a user (can rejoin) |
| `/stats` | Show group moderation statistics |
| `/settings` | Configure bot settings for this group |

---

## Inline Moderation Actions

When spam is detected, an inline keyboard is sent to the admin:

| Button | Action |
|---|---|
| 🗑 Delete message | Delete the flagged message |
| ✅ Not spam | Mark as false positive |
| ⚠️ Warn user | Issue a warning |
| 🔇 Mute 10 min | Mute the user |
| 🚫 Ban user | Permanently ban the user |

---

## API Integration

The bot communicates with the FindSpam backend API:

| Endpoint | Usage |
|---|---|
| `POST /ai/predict` | Text spam classification |
| `POST /moderation/events` | Log moderation action |
| `GET /blacklist/domains/check` | Domain blacklist check |
| `GET /telegram/groups/{id}/settings` | Fetch group configuration |
| `PUT /telegram/groups/{id}/settings` | Update group configuration |
| `GET /telegram/groups/{id}/stats` | Fetch group statistics |
| `GET /telegram/users/{id}` | Fetch user profile |

---

## Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run bot (polling mode)
python main.py

# Lint
ruff check .

# Type check
mypy .

# Tests
pytest
```

---

## Extending the Bot

- **Add a command**: create a handler in `handlers/commands/`, include router in `core/setup.py`
- **Add a filter**: implement `Filter` subclass in `filters/`, apply to handler decorators
- **Add a middleware**: implement `BaseMiddleware` in `middlewares/`, register in `core/setup.py`
- **Add a service**: implement in `services/`, inject via `data["key"]` in handlers
- **Add a locale**: create `locales/{lang}.py`, register mapping in `locales/__init__.py`
