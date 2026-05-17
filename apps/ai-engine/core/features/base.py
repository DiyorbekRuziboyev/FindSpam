from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np


@dataclass
class FeatureVector:
    name: str
    features: np.ndarray
    feature_names: list[str] = field(default_factory=list)


class BaseFeatureExtractor(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def extract(self, text: str, **context: object) -> FeatureVector: ...

    def fit(self, texts: list[str]) -> None:
        """Override to support supervised fitting (e.g. TF-IDF vocabulary training)."""
