import logging
from typing import Dict, Any
from app.ai.mastery.predictor import MasteryPredictor
from app.ai.mastery.model_loader import MasteryModelLoader
from app.ai.mastery.schemas import MasteryPredictionRequest, MasteryPredictionResponse

logger = logging.getLogger("mindtrace.ai.mastery.service")

class MasteryService:
    def __init__(self):
        self.predictor = MasteryPredictor()

    def predict_mastery(self, request: MasteryPredictionRequest) -> MasteryPredictionResponse:
        mastery, prob_success, trend = self.predictor.predict_mastery(request)
        return MasteryPredictionResponse(
            concept=request.concept or "Mathematics",
            mastery=mastery,
            probability_of_success=prob_success,
            trend=trend,
            model_name="MindTrace Mastery Predictor"
        )

    def get_model_info(self) -> Dict[str, Any]:
        _, _, metadata = MasteryModelLoader.load_mastery_model()
        return metadata

_mastery_service_instance = None

def get_mastery_service() -> MasteryService:
    global _mastery_service_instance
    if _mastery_service_instance is None:
        _mastery_service_instance = MasteryService()
    return _mastery_service_instance
