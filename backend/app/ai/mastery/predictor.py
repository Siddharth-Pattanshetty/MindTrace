import logging
import xgboost as xgb
import pandas as pd
from typing import Tuple
from app.ai.mastery.model_loader import MasteryModelLoader
from app.ai.mastery.feature_builder import MasteryFeatureBuilder
from app.ai.mastery.schemas import MasteryPredictionRequest

logger = logging.getLogger("mindtrace.ai.mastery.predictor")

class MasteryPredictor:
    def __init__(self):
        self.model, self.booster, self.metadata = MasteryModelLoader.load_mastery_model()
        self.feature_builder = MasteryFeatureBuilder()

    def predict_mastery(self, request: MasteryPredictionRequest) -> Tuple[float, float, str]:
        """
        Predicts student probability of success and maps it to mastery score and trend.
        Returns: (mastery_score, probability_of_success, trend)
        """
        try:
            df_features = self.feature_builder.build_features(request)
            dmatrix = xgb.DMatrix(df_features, feature_names=list(df_features.columns))
            raw_prob = float(self.booster.predict(dmatrix)[0])
            
            # Clip bounds
            prob_success = max(0.0, min(1.0, raw_prob))
            mastery_score = prob_success  # V1 representation

            recent = request.recent_accuracy if request.recent_accuracy is not None else 0.70
            prev = request.previous_accuracy if request.previous_accuracy is not None else 0.70

            if recent > prev + 0.05:
                trend = "improving"
            elif recent < prev - 0.05:
                trend = "declining"
            else:
                trend = "stable"

            return round(mastery_score, 4), round(prob_success, 4), trend

        except Exception as e:
            logger.error(f"Error executing mastery prediction: {e}", exc_info=True)
            fallback_prob = float(request.recent_accuracy or 0.70)
            return round(fallback_prob, 4), round(fallback_prob, 4), "stable"
