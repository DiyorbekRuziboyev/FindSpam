from core.features.base import BaseFeatureExtractor


class FeatureRegistry:
    def __init__(self) -> None:
        self._extractors: dict[str, BaseFeatureExtractor] = {}

    def register(self, extractor: BaseFeatureExtractor) -> None:
        self._extractors[extractor.name] = extractor

    def get(self, name: str) -> BaseFeatureExtractor:
        extractor = self._extractors.get(name)
        if extractor is None:
            raise KeyError(f"Feature extractor '{name}' not registered")
        return extractor

    def all(self) -> list[BaseFeatureExtractor]:
        return list(self._extractors.values())

    @classmethod
    def default(cls) -> "FeatureRegistry":
        from core.features.linguistic import LinguisticFeatureExtractor
        from core.features.url import URLFeatureExtractor
        from core.features.tfidf import TFIDFFeatureExtractor

        registry = cls()
        registry.register(LinguisticFeatureExtractor())
        registry.register(URLFeatureExtractor())
        registry.register(TFIDFFeatureExtractor())
        return registry
