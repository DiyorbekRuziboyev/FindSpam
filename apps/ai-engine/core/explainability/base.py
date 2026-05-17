from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ExplanationToken:
    token: str
    importance: float
    is_spam_signal: bool


@dataclass
class Explanation:
    top_tokens: list[ExplanationToken]
    triggered_rules: list[str]
    model_contributions: dict[str, float]
    summary: str
    raw: dict = field(default_factory=dict)


class BaseExplainer(ABC):
    @abstractmethod
    def explain(
        self,
        text: str,
        model_contributions: dict[str, float],
        spam_score: float,
        category: str | None,
    ) -> Explanation: ...
