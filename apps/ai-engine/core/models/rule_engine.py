import re
import logging
from dataclasses import dataclass

from core.models.base import BaseModelAdapter, ModelPrediction

logger = logging.getLogger(__name__)


@dataclass
class _Rule:
    name: str
    pattern: re.Pattern[str]
    category: str
    weight: float


_RULES: list[_Rule] = [
    _Rule("phishing_url", re.compile(r"https?://\d{1,3}(?:\.\d{1,3}){3}", re.IGNORECASE), "PHISHING", 0.9),
    _Rule("telegram_invite_spam", re.compile(r"t\.me/joinchat/[A-Za-z0-9_-]+", re.IGNORECASE), "SCAM", 0.75),
    _Rule("crypto_profit_promise", re.compile(r"(earn|make|get)\s+\$?\d+\s*(btc|eth|usdt|bitcoin|ethereum)\s*(per|a|every)\s*(day|week|month)", re.IGNORECASE), "SCAM", 0.85),
    _Rule("prize_claim", re.compile(r"(you'?ve?|you\s+have)\s+(won|been\s+selected|been\s+chosen)\s+(a\s+prize|a\s+reward|\$\d+|cash)", re.IGNORECASE), "FAKE_GIVEAWAY", 0.90),
    _Rule("urgency_manipulation", re.compile(r"(act\s+now|limited\s+time|expires?\s+in\s+\d+|today\s+only|last\s+chance|срочно|tezkor|shoshiling)", re.IGNORECASE), "ADVERTISEMENT", 0.60),
    _Rule("free_money", re.compile(r"(free\s+money|бесплатные\s+деньги|бесплатный\s+кредит|tekin\s+pul)", re.IGNORECASE), "SCAM", 0.85),
    _Rule("password_request", re.compile(r"(send|share|enter|provide)\s+(your\s+)?(password|паролингиз|parol|pin\s*code)", re.IGNORECASE), "PHISHING", 0.95),
    _Rule("financial_data_request", re.compile(r"(credit\s+card|bank\s+account|card\s+number|cvv|ssn|passport\s+number)", re.IGNORECASE), "PHISHING", 0.90),
    _Rule("pyramid_scheme", re.compile(r"(refer\s+\d+\s+friends?|invite\s+\d+\s+people|recruit\s+\d+\s+members?)\s+(to\s+earn|and\s+earn|for\s+(free|cash))", re.IGNORECASE), "SCAM", 0.80),
    _Rule("brand_impersonation", re.compile(r"(paypa1|g00gle|faceb00k|amaz0n|appl3|telegr4m)\b", re.IGNORECASE), "PHISHING", 0.92),
    _Rule("suspicious_shortlink", re.compile(r"https?://(bit\.ly|tinyurl\.com|ow\.ly|is\.gd|cutt\.ly)/[A-Za-z0-9]+", re.IGNORECASE), "SUSPICIOUS_URL", 0.55),
    _Rule("investment_scam", re.compile(r"(guaranteed\s+profit|risk.?free\s+investment|100\s*%\s+return|passive\s+income\s+of\s+\$?\d+)", re.IGNORECASE), "SCAM", 0.88),
]

_SPAM_CATEGORIES = {rule.category for rule in _RULES}


class RuleEngine(BaseModelAdapter):
    @property
    def name(self) -> str:
        return "rule_engine"

    def load(self) -> None:
        self._is_loaded = True
        logger.info("Rule engine loaded", extra={"rules": len(_RULES)})

    async def predict(self, text: str) -> ModelPrediction:
        if not self._is_loaded:
            return self.stub_prediction()

        if not text or not text.strip():
            return ModelPrediction(
                spam_probability=0.0,
                category_scores={cat: 0.0 for cat in _SPAM_CATEGORIES},
                is_loaded=True,
                model_name=self.name,
            )

        category_max: dict[str, float] = {cat: 0.0 for cat in _SPAM_CATEGORIES}
        matched_weights: list[float] = []

        for rule in _RULES:
            if rule.pattern.search(text):
                matched_weights.append(rule.weight)
                category_max[rule.category] = max(category_max[rule.category], rule.weight)

        if matched_weights:
            combined = 1.0 - 1.0
            score = 1.0
            for w in matched_weights:
                score *= 1.0 - w
            spam_probability = 1.0 - score
        else:
            spam_probability = 0.0

        return ModelPrediction(
            spam_probability=min(spam_probability, 1.0),
            category_scores=category_max,
            is_loaded=True,
            model_name=self.name,
        )
