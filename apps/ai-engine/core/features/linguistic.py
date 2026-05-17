import re

import numpy as np

from core.features.base import BaseFeatureExtractor, FeatureVector

_SPAM_KEYWORDS: list[str] = [
    # Russian spam keywords
    "бесплатно", "выиграй", "заработай", "скидка", "акция", "казино",
    "кредит", "займ", "инвестиции", "заработок", "доход",
    # Uzbek Latin spam keywords
    "bepul", "yutib oling", "daromad", "kredit", "aksiya", "chegirma",
    "ishlang", "foydali", "investitsiya", "pul topish",
    # English spam keywords
    "free", "winner", "earn", "casino", "loan", "investment",
    "income", "profit", "click here", "limited offer", "act now",
]

_SCAM_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"guaranteed\s+(profit|income|return)", re.IGNORECASE),
    re.compile(r"(make|earn)\s+\$?\d+\s*(per|a)\s*(day|week|month)", re.IGNORECASE),
    re.compile(r"risk.?free", re.IGNORECASE),
    re.compile(r"100\s*%\s*(guaranteed|profit)", re.IGNORECASE),
    re.compile(r"(your|you'?ve)\s+(won|been\s+selected|been\s+chosen)", re.IGNORECASE),
    re.compile(r"(send|transfer)\s+(money|bitcoin|crypto|btc)", re.IGNORECASE),
]

_FEATURE_NAMES = [
    "spam_keyword_density",
    "scam_pattern_count",
    "caps_ratio",
    "exclamation_density",
    "url_density",
    "digit_ratio",
    "avg_word_length",
    "repetition_ratio",
    "question_density",
    "has_urgency",
]

_URGENCY_RE = re.compile(
    r"\b(urgent|hurry|limited|expires|today\s+only|last\s+chance|now\s+or\s+never|срочно|только\s+сегодня|tezkor|shoshiling)\b",
    re.IGNORECASE,
)


class LinguisticFeatureExtractor(BaseFeatureExtractor):
    @property
    def name(self) -> str:
        return "linguistic"

    def extract(self, text: str, **context: object) -> FeatureVector:
        if not text:
            return FeatureVector(name=self.name, features=np.zeros(len(_FEATURE_NAMES), dtype=np.float32), feature_names=_FEATURE_NAMES)

        words = text.split()
        word_count = max(len(words), 1)
        char_count = max(len(text), 1)

        lower = text.lower()
        keyword_hits = sum(1 for kw in _SPAM_KEYWORDS if kw in lower)
        scam_hits = sum(1 for p in _SCAM_PATTERNS if p.search(text))

        alpha_chars = [c for c in text if c.isalpha()]
        upper_chars = [c for c in alpha_chars if c.isupper()]
        caps_ratio = len(upper_chars) / max(len(alpha_chars), 1)

        exclamation_density = text.count("!") / char_count
        url_density = (text.count("http") + text.count("www.")) / word_count
        digit_ratio = sum(c.isdigit() for c in text) / char_count
        avg_word_length = sum(len(w) for w in words) / word_count

        word_set = set(words)
        repetition_ratio = 1.0 - (len(word_set) / word_count)
        question_density = text.count("?") / char_count
        has_urgency = 1.0 if _URGENCY_RE.search(text) else 0.0

        features = np.array(
            [
                keyword_hits / word_count,
                min(scam_hits, 5) / 5.0,
                caps_ratio,
                exclamation_density,
                url_density,
                digit_ratio,
                min(avg_word_length, 15.0) / 15.0,
                repetition_ratio,
                question_density,
                has_urgency,
            ],
            dtype=np.float32,
        )

        return FeatureVector(name=self.name, features=features, feature_names=_FEATURE_NAMES)
