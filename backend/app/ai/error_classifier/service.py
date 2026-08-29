import logging
from typing import Dict, Any, Tuple
from app.ai.error_classifier.predictor import ErrorClassifierPredictor
from app.ai.error_classifier.model_loader import ErrorClassifierModelLoader
from app.ai.error_classifier.schemas import ErrorClassificationRequest, ErrorClassificationResponse, ModelInfoResponse

logger = logging.getLogger("mindtrace.error_classifier.service")

class ErrorClassifierService:
    def __init__(self):
        self.predictor = ErrorClassifierPredictor()

    def classify_error(self, request: ErrorClassificationRequest) -> ErrorClassificationResponse:
        error_type, confidence = self.predictor.predict(
            question=request.question,
            student_answer=request.student_answer,
            work_evidence=request.work_evidence or ""
        )
        return ErrorClassificationResponse(
            error_type=error_type,
            confidence=round(confidence, 4)
        )

    def get_model_info(self) -> ModelInfoResponse:
        metadata = ErrorClassifierModelLoader.get_metadata()
        vectorizer, classifier, classes, _ = ErrorClassifierModelLoader.load_model()
        return ModelInfoResponse(
            model_name=metadata.get("model_name", "MindTrace Error Classifier"),
            version=metadata.get("version", "1.0.0"),
            algorithm=metadata.get("algorithm", "TF-IDF + Logistic Regression"),
            dataset=metadata.get("dataset", "MAP"),
            classes=classes if isinstance(classes, list) else list(classes or []),
            metadata={"evaluation_metrics": metadata.get("evaluation_metrics", {})}
        )

# Singleton instance for service reuse
_error_classifier_service = None

def get_error_classifier_service() -> ErrorClassifierService:
    global _error_classifier_service
    if _error_classifier_service is None:
        _error_classifier_service = ErrorClassifierService()
    return _error_classifier_service
