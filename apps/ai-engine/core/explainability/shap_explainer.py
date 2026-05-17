import asyncio
import logging

from core.explainability.base import BaseExplainer, Explanation, ExplanationToken
from core.explainability.feature_explainer import FeatureImportanceExplainer

logger = logging.getLogger(__name__)


class SHAPExplainer(BaseExplainer):
    """SHAP-based explainer for the TF-IDF + LogisticRegression pipeline.

    Falls back to FeatureImportanceExplainer when the sklearn pipeline
    is unavailable (model artifacts not yet trained).
    """

    def __init__(self, tfidf_lr_pipeline=None) -> None:
        self._pipeline = tfidf_lr_pipeline
        self._explainer = None
        self._fallback = FeatureImportanceExplainer()

    def _build_shap_explainer(self) -> None:
        if self._pipeline is None or self._explainer is not None:
            return
        try:
            import shap

            vectorizer = self._pipeline.named_steps["tfidf"]
            lr = self._pipeline.named_steps["lr"]
            self._explainer = shap.LinearExplainer(lr, shap.sample(vectorizer.transform([""]), 1))
        except Exception:
            logger.warning("Failed to initialize SHAP explainer; falling back to feature importance", exc_info=True)

    def _sync_explain(
        self,
        text: str,
        model_contributions: dict[str, float],
        spam_score: float,
        category: str | None,
    ) -> Explanation:
        if self._pipeline is None:
            return self._fallback.explain(text, model_contributions, spam_score, category)

        try:
            import shap
            import numpy as np

            self._build_shap_explainer()
            if self._explainer is None:
                return self._fallback.explain(text, model_contributions, spam_score, category)

            vectorizer = self._pipeline.named_steps["tfidf"]
            features = vectorizer.transform([text])
            shap_values = self._explainer.shap_values(features)

            if isinstance(shap_values, list):
                values = shap_values[1][0] if len(shap_values) > 1 else shap_values[0][0]
            else:
                values = shap_values[0]

            feature_names = vectorizer.get_feature_names_out()
            top_indices = np.argsort(np.abs(values))[::-1][:10]

            tokens = [
                ExplanationToken(
                    token=feature_names[i],
                    importance=float(abs(values[i])),
                    is_spam_signal=values[i] > 0,
                )
                for i in top_indices
                if abs(values[i]) > 1e-6
            ]

            base = self._fallback.explain(text, model_contributions, spam_score, category)
            return Explanation(
                top_tokens=tokens,
                triggered_rules=base.triggered_rules,
                model_contributions=model_contributions,
                summary=base.summary,
                raw={"shap_values": values.tolist()[:20], "spam_score": spam_score},
            )
        except Exception:
            logger.warning("SHAP explanation failed; using fallback", exc_info=True)
            return self._fallback.explain(text, model_contributions, spam_score, category)

    def explain(
        self,
        text: str,
        model_contributions: dict[str, float],
        spam_score: float,
        category: str | None,
    ) -> Explanation:
        return self._sync_explain(text, model_contributions, spam_score, category)

    async def explain_async(
        self,
        text: str,
        model_contributions: dict[str, float],
        spam_score: float,
        category: str | None,
    ) -> Explanation:
        return await asyncio.to_thread(self._sync_explain, text, model_contributions, spam_score, category)
