import asyncio
import logging
from pathlib import Path

from core.models.base import BaseModelAdapter, ModelPrediction

logger = logging.getLogger(__name__)

_LOCAL_MODEL_DIR = Path(__file__).parents[3] / "model_artifacts" / "xlm_roberta"

_CATEGORIES = ["SCAM", "PHISHING", "ADVERTISEMENT", "FAKE_GIVEAWAY", "SOCIAL_ENGINEERING", "SUSPICIOUS_URL", "OTHER"]
_HAM_IDX = 0
_SPAM_IDX = 1


class XLMRobertaAdapter(BaseModelAdapter):
    def __init__(self, model_name: str = "xlm-roberta-base", max_length: int = 512) -> None:
        self._model_name = model_name
        self._max_length = max_length
        self._tokenizer = None
        self._model = None
        self._device = "cpu"

    @property
    def name(self) -> str:
        return "xlm_roberta"

    def load(self) -> None:
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForSequenceClassification

            self._device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info("XLM-RoBERTa loading", extra={"device": self._device, "model": self._model_name})

            source = str(_LOCAL_MODEL_DIR) if _LOCAL_MODEL_DIR.exists() else self._model_name

            self._tokenizer = AutoTokenizer.from_pretrained(source)
            self._model = AutoModelForSequenceClassification.from_pretrained(source)
            self._model.to(self._device)
            self._model.eval()

            self._is_loaded = True
            logger.info("XLM-RoBERTa loaded", extra={"source": source, "device": self._device})
        except Exception:
            logger.warning(
                "XLM-RoBERTa failed to load; adapter will return stub predictions. "
                "Rule engine + TF-IDF remain active.",
                exc_info=True,
            )

    def _sync_predict_batch(self, texts: list[str]) -> list[ModelPrediction]:
        import torch
        import torch.nn.functional as F

        inputs = self._tokenizer(
            texts,
            return_tensors="pt",
            truncation=True,
            max_length=self._max_length,
            padding=True,
        )
        inputs = {k: v.to(self._device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self._model(**inputs)

        probas = F.softmax(outputs.logits, dim=-1).cpu().numpy()

        results = []
        for proba in probas:
            spam_prob = float(proba[_SPAM_IDX]) if proba.shape[0] > 1 else float(proba[0])
            category_scores = {cat: spam_prob / len(_CATEGORIES) for cat in _CATEGORIES}
            results.append(
                ModelPrediction(
                    spam_probability=spam_prob,
                    category_scores=category_scores,
                    is_loaded=True,
                    model_name=self.name,
                    raw_logits=proba.tolist(),
                )
            )
        return results

    async def predict(self, text: str) -> ModelPrediction:
        if not self._is_loaded:
            return self.stub_prediction()
        results = await asyncio.to_thread(self._sync_predict_batch, [text])
        return results[0]

    async def predict_batch(self, texts: list[str]) -> list[ModelPrediction]:
        if not self._is_loaded:
            return [self.stub_prediction() for _ in texts]
        return await asyncio.to_thread(self._sync_predict_batch, texts)
