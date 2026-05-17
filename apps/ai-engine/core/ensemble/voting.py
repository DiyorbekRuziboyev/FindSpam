from core.ensemble.base import BaseEnsembleStrategy, EnsembleResult
from core.models.base import ModelPrediction

_SPAM_THRESHOLD = 0.5


class MajorityVotingEnsemble(BaseEnsembleStrategy):
    def combine(
        self,
        predictions: dict[str, ModelPrediction],
        weights: dict[str, float],
    ) -> EnsembleResult:
        loaded = {name: pred for name, pred in predictions.items() if pred.is_loaded}
        contributions: dict[str, float] = {name: (pred.spam_probability if pred.is_loaded else 0.0) for name, pred in predictions.items()}

        if not loaded:
            return EnsembleResult(final_score=0.0, category=None, contributions=contributions)

        spam_votes = sum(1 for pred in loaded.values() if pred.spam_probability >= _SPAM_THRESHOLD)
        final_score = spam_votes / len(loaded)

        category_votes: dict[str, int] = {}
        for pred in loaded.values():
            if pred.category_scores:
                top_cat = max(pred.category_scores, key=lambda k: pred.category_scores[k])
                category_votes[top_cat] = category_votes.get(top_cat, 0) + 1

        top_category = max(category_votes, key=lambda k: category_votes[k]) if category_votes else None

        return EnsembleResult(
            final_score=final_score,
            category=top_category,
            contributions=contributions,
        )
