import logging

from core.models.base import BaseModelAdapter

logger = logging.getLogger(__name__)


class ModelRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, BaseModelAdapter] = {}

    def register(self, adapter: BaseModelAdapter) -> None:
        self._adapters[adapter.name] = adapter

    def get(self, name: str) -> BaseModelAdapter:
        adapter = self._adapters.get(name)
        if adapter is None:
            raise KeyError(f"Model adapter '{name}' not registered")
        return adapter

    def all(self) -> list[BaseModelAdapter]:
        return list(self._adapters.values())

    def load_all(self) -> dict[str, bool]:
        results: dict[str, bool] = {}
        for adapter in self._adapters.values():
            try:
                adapter.load()
                results[adapter.name] = adapter.is_loaded
                logger.info("Model load completed", extra={"model": adapter.name, "loaded": adapter.is_loaded})
            except Exception:
                results[adapter.name] = False
                logger.exception("Model load raised unexpectedly", extra={"model": adapter.name})
        return results

    @classmethod
    def default(cls) -> "ModelRegistry":
        from core.models.rule_engine import RuleEngine
        from core.models.tfidf_lr import TFIDFLogisticRegressionAdapter
        from core.models.xlm_roberta import XLMRobertaAdapter
        from core.models.mbert import MultilingualBERTAdapter
        from core.config import get_ai_settings

        settings = get_ai_settings()
        registry = cls()
        registry.register(RuleEngine())
        registry.register(TFIDFLogisticRegressionAdapter())
        registry.register(XLMRobertaAdapter(model_name=settings.xlm_roberta_model, max_length=settings.max_seq_length))
        registry.register(MultilingualBERTAdapter(model_name=settings.mbert_model, max_length=settings.max_seq_length))
        return registry
