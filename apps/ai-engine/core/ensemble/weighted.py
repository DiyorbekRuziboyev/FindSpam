from core.ensemble.base import BaseEnsembleStrategy, EnsembleResult
from core.models.base import ModelPrediction


class WeightedAverageEnsemble(BaseEnsembleStrategy):
    def combine(
        self,
        predictions: dict[str, ModelPrediction],
        weights: dict[str, float],
    ) -> EnsembleResult:
        total_weight = 0.0
        weighted_score = 0.0
        contributions: dict[str, float] = {}
        category_accumulator: dict[str, float] = {}

        for model_name, prediction in predictions.items():
            w = weights.get(model_name, 0.0)
            if not prediction.is_loaded:
                contributions[model_name] = 0.0
                continue

            weighted_score += prediction.spam_probability * w
            total_weight += w
            contributions[model_name] = prediction.spam_probability * w

            for cat, score in prediction.category_scores.items():
                category_accumulator[cat] = category_accumulator.get(cat, 0.0) + score * w

        if total_weight == 0.0:
            return EnsembleResult(final_score=0.0, category=None, contributions=contributions)

        final_score = weighted_score / total_weight

        top_category: str | None = None
        if category_accumulator:
            top_category = max(category_accumulator, key=lambda k: category_accumulator[k])
            if category_accumulator[top_category] / total_weight < 0.05:
                top_category = None

        return EnsembleResult(
            final_score=min(final_score, 1.0),
            category=top_category,
            contributions=contributions,
        )
