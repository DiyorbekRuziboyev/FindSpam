from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ModelPrediction:
    spam_probability: float
    category_scores: dict[str, float]
    is_loaded: bool
    model_name: str
    raw_logits: list[float] = field(default_factory=list)


class ModelNotLoadedError(RuntimeError):
    pass


class BaseModelAdapter(ABC):
    _is_loaded: bool = False

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def load(self) -> None:
        """Lazy-initialize model artifacts. Called during application lifespan startup.
        Must be safe to skip — adapter returns stub prediction when not loaded."""

    @abstractmethod
    async def predict(self, text: str) -> ModelPrediction: ...

    async def predict_batch(self, texts: list[str]) -> list[ModelPrediction]:
        results = []
        for text in texts:
            results.append(await self.predict(text))
        return results

    def stub_prediction(self) -> ModelPrediction:
        return ModelPrediction(
            spam_probability=0.0,
            category_scores={},
            is_loaded=False,
            model_name=self.name,
        )

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded
