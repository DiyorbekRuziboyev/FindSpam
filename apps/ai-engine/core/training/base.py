from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TrainingConfig:
    model_name: str
    max_features: int = 10000
    ngram_range: tuple[int, int] = (1, 2)
    test_size: float = 0.2
    random_state: int = 42
    min_samples: int = 500


@dataclass
class TrainingResult:
    model_name: str
    accuracy: float
    f1_score: float
    precision: float
    recall: float
    samples_used: int
    trained_at: datetime = field(default_factory=datetime.utcnow)
    artifact_path: str = ""


class BaseTrainer(ABC):
    def __init__(self, config: TrainingConfig) -> None:
        self.config = config

    @abstractmethod
    def train(self, texts: list[str], labels: list[int]) -> TrainingResult: ...

    @abstractmethod
    def evaluate(self, texts: list[str], labels: list[int]) -> TrainingResult: ...
