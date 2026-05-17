import re

from core.explainability.base import BaseExplainer, Explanation, ExplanationToken

_SPAM_SIGNALS: list[tuple[str, float]] = [
    ("free", 0.7), ("бесплатно", 0.7), ("bepul", 0.7),
    ("win", 0.75), ("выиграй", 0.75), ("yutib", 0.75),
    ("earn", 0.65), ("заработай", 0.65), ("ishlang", 0.65),
    ("casino", 0.8), ("казино", 0.8),
    ("bitcoin", 0.72), ("btc", 0.72), ("crypto", 0.68),
    ("click here", 0.6), ("act now", 0.65), ("срочно", 0.65),
    ("guaranteed", 0.78), ("profit", 0.6), ("investment", 0.55),
    ("loan", 0.6), ("кредит", 0.6), ("kredit", 0.6),
    ("password", 0.9), ("паролингиз", 0.9), ("parol", 0.9),
    ("limited offer", 0.7), ("expires", 0.55),
]

_RULE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("IP address URL", re.compile(r"https?://\d{1,3}(?:\.\d{1,3}){3}")),
    ("Telegram invite link", re.compile(r"t\.me/joinchat/")),
    ("Crypto profit promise", re.compile(r"(earn|make|get)\s+\$?\d+\s*(btc|eth|usdt)", re.IGNORECASE)),
    ("Prize/giveaway claim", re.compile(r"(you'?ve?|you\s+have)\s+(won|been\s+selected)", re.IGNORECASE)),
    ("Urgency trigger", re.compile(r"(act\s+now|limited\s+time|today\s+only|last\s+chance|срочно|tezkor)", re.IGNORECASE)),
    ("Password/credential request", re.compile(r"(send|share|provide)\s+(your\s+)?(password|pin|parol)", re.IGNORECASE)),
    ("Investment scam", re.compile(r"(guaranteed\s+profit|risk.?free|100\s*%\s+return)", re.IGNORECASE)),
    ("Brand impersonation", re.compile(r"(paypa1|g00gle|faceb00k|amaz0n|appl3)", re.IGNORECASE)),
    ("URL shortener", re.compile(r"https?://(bit\.ly|tinyurl\.com|ow\.ly)/", re.IGNORECASE)),
]


class FeatureImportanceExplainer(BaseExplainer):
    def explain(
        self,
        text: str,
        model_contributions: dict[str, float],
        spam_score: float,
        category: str | None,
    ) -> Explanation:
        lower = text.lower()

        tokens: list[ExplanationToken] = []
        for signal, importance in _SPAM_SIGNALS:
            if signal in lower:
                tokens.append(ExplanationToken(token=signal, importance=importance, is_spam_signal=True))

        tokens.sort(key=lambda t: t.importance, reverse=True)
        top_tokens = tokens[:10]

        triggered_rules: list[str] = []
        for rule_name, pattern in _RULE_PATTERNS:
            if pattern.search(text):
                triggered_rules.append(rule_name)

        if spam_score >= 0.80:
            confidence_label = "high confidence"
        elif spam_score >= 0.60:
            confidence_label = "moderate confidence"
        else:
            confidence_label = "low confidence"

        parts: list[str] = [f"Classified as {'spam' if spam_score >= 0.5 else 'legitimate'} with {confidence_label} ({spam_score:.0%} score)."]
        if category:
            parts.append(f"Category: {category}.")
        if triggered_rules:
            parts.append(f"Triggered rules: {', '.join(triggered_rules[:3])}.")
        if top_tokens:
            signal_words = ", ".join(f"'{t.token}'" for t in top_tokens[:5])
            parts.append(f"Spam signals detected: {signal_words}.")

        return Explanation(
            top_tokens=top_tokens,
            triggered_rules=triggered_rules,
            model_contributions=model_contributions,
            summary=" ".join(parts),
            raw={"spam_score": spam_score, "category": category},
        )
