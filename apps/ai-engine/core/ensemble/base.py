from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.models.base import ModelPrediction


@dataclass
class EnsembleResult:
    final_score: float
    category: str | None
    contributions: dict[str, float]


class BaseEnsembleStrategy(ABC):
    @abstractmethod
    def combine(
        self,
        predictions: dict[str, ModelPrediction],
        weights: dict[str, float],
    ) -> EnsembleResult: ...
