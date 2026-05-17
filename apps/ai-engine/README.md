# FindSpam AI Engine

Hybrid ensemble AI inference service for multilingual spam, scam, and phishing detection.

---

## Architecture

```
ai-engine/
├── core/
│   ├── config.py              # AIEngineSettings (pydantic-settings)
│   ├── preprocessor/          # Text normalization, language detection, entity extraction
│   ├── features/              # Feature extractors: linguistic, URL, TF-IDF
│   ├── models/                # Model adapters with lazy .load()
│   ├── ensemble/              # Weighted average + majority voting strategies
│   ├── explainability/        # SHAP + feature-importance explainers
│   ├── serving/               # Orchestrator, Redis cache, batch predictor
│   └── training/              # Feedback collector, retraining pipeline
├── api/
│   ├── schemas.py             # Pydantic v2 request/response models
│   └── router.py              # FastAPI routes: /predict, /predict/batch, /feedback, /health
├── monitoring/
│   ├── metrics.py             # Sliding-window inference metrics (p95 latency, spam rate)
│   └── audit.py              # Daily JSONL audit trail (text_hash, not raw text)
├── model_artifacts/           # Saved .joblib and HuggingFace model directories
├── data/
│   ├── feedback/              # JSONL feedback for retraining (feedback_YYYY-MM-DD.jsonl)
│   └── audit/                 # JSONL audit logs (audit_YYYY-MM-DD.jsonl)
└── main.py                    # FastAPI app with lifespan startup
```

---

## Ensemble Design

| Model | Weight | Notes |
|---|---|---|
| XLM-RoBERTa | 0.40 | Semantic understanding, multilingual |
| mBERT | 0.25 | Multilingual BERT, cross-lingual transfer |
| TF-IDF + LogReg | 0.20 | Fast baseline, retrainable from feedback |
| Rule Engine | 0.15 | 12 compiled regex rules, zero dependencies |

When transformer models are absent (no artifacts downloaded), weight is redistributed to loaded models. The system is always operational via Rule Engine + TF-IDF.

---

## Supported Languages

- Uzbek Latin (`uz_latin`)
- Uzbek Cyrillic (`uz_cyrillic`) — disambiguated from Uzbek Latin via Cyrillic-character-ratio heuristic (>25% threshold)
- Russian (`ru`)
- English (`en`)

---

## Spam Categories

| API Category | Description |
|---|---|
| `SCAM` | Investment fraud, fake profits, pyramid schemes |
| `PHISHING` | Credential theft, brand impersonation, IP-address URLs |
| `MALICIOUS_AD` | Unsolicited commercial advertising |
| `FAKE_GIVEAWAY` | Prize/lottery scams |
| `SOCIAL_ENGINEERING` | Psychological manipulation |
| `SUSPICIOUS_URL` | Shortlinks, suspicious TLDs, IP-address links |
| `OTHER` | Uncategorized spam |

---

## Threat Levels

| Score | Level |
|---|---|
| ≥ 0.95 | `CRITICAL` |
| 0.80 – 0.94 | `HIGH` |
| 0.60 – 0.79 | `MEDIUM` |
| 0.30 – 0.59 | `LOW` |
| < 0.30 | `NONE` |

---

## API Endpoints

```
POST /api/v1/predict          — Single text prediction
POST /api/v1/predict/batch    — Batch prediction (max 100 texts, chunked by 32)
POST /api/v1/feedback         — Submit correction for retraining
GET  /api/v1/health           — Model load status + service health
```

### Example: Single Prediction

```json
POST /api/v1/predict
{
  "text": "You have won $10,000! Click here to claim your prize now.",
  "metadata": {}
}

Response:
{
  "is_spam": true,
  "confidence": 0.91,
  "threat_level": "HIGH",
  "spam_category": "FAKE_GIVEAWAY",
  "model_contributions": {
    "xlm_roberta": 0.38,
    "mbert": 0.22,
    "tfidf_lr": 0.18,
    "rule_engine": 0.13
  },
  "explanation": {
    "summary": "Classified as spam with high confidence (91% score). Category: FAKE_GIVEAWAY. Triggered rules: Prize/giveaway claim, Urgency trigger.",
    "triggered_rules": ["Prize/giveaway claim", "Urgency trigger"],
    "top_tokens": [{"token": "won", "importance": 0.75}, {"token": "click here", "importance": 0.6}]
  },
  "processing_ms": 42.5
}
```

---

## Configuration

All settings via environment variables (`.env` file or shell exports):

```env
DEBUG=false
HOST=0.0.0.0
PORT=8001

XLM_ROBERTA_MODEL=xlm-roberta-base
MBERT_MODEL=bert-base-multilingual-cased
MAX_SEQ_LENGTH=512
BATCH_SIZE=32

WEIGHT_XLM_ROBERTA=0.40
WEIGHT_MBERT=0.25
WEIGHT_TFIDF_LR=0.20
WEIGHT_RULE_ENGINE=0.15

THRESHOLD_SPAM=0.80
THRESHOLD_SUSPICIOUS=0.60
THRESHOLD_REVIEW=0.30

REDIS_URL=redis://localhost:6379/0
PREDICTION_CACHE_TTL=3600
```

---

## Model Artifacts

Place pre-trained artifacts in `model_artifacts/`:

```
model_artifacts/
├── tfidf_lr_pipeline.joblib    # TF-IDF + LogisticRegression sklearn pipeline
├── tfidf_vectorizer.joblib     # Standalone TF-IDF vectorizer (feature extractor)
├── xlm_roberta/                # Fine-tuned XLM-RoBERTa (HuggingFace format)
└── mbert/                      # Fine-tuned mBERT (HuggingFace format)
```

If transformer artifact directories are absent, the engine loads from HuggingFace Hub using the configured model name. The engine is fully operational without any artifacts — Rule Engine and TF-IDF serve responses immediately.

---

## Feedback & Retraining

```python
# Submit correction via API
POST /api/v1/feedback
{
  "text": "...",
  "predicted_spam": true,
  "is_spam": false,   # correction
  "confidence": 0.83,
  "source": "moderator"
}
```

Feedback accumulates in `data/feedback/feedback_YYYY-MM-DD.jsonl`. When ≥ 500 samples are collected, `RetrainingPipeline.run()` triggers TF-IDF + LogReg retraining and saves the updated artifact.

---

## Inference Cache

Predictions are cached in Redis using key `pred:{model_version}:{sha256(text)}`. Cache TTL is configurable (default 3600s). If Redis is unavailable, predictions proceed without caching — no errors surface to the caller.

---

## Audit Trail

Every prediction is written to `data/audit/audit_YYYY-MM-DD.jsonl` with:
- `text_hash` (SHA-256) — never the raw text
- `confidence`, `threat_level`, `spam_category`
- `model_contributions` (per-model weighted scores)
- `processing_ms`, `audited_at`

---

## Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run with auto-reload
python main.py

# Lint
ruff check .

# Type check
mypy .

# Tests
pytest
```

---

## Extending the Engine

- **Add a model**: implement `BaseModelAdapter` in `core/models/`, register in `ModelRegistry.default()`
- **Add a feature extractor**: implement `BaseFeatureExtractor` in `core/features/`, register in `FeatureRegistry.default()`
- **Add an ensemble strategy**: implement `BaseEnsembleStrategy` in `core/ensemble/`, pass to `EnsemblePredictor`
- **Add an explainer**: implement `BaseExplainer` in `core/explainability/`, pass via `predictor.set_explainer()`
