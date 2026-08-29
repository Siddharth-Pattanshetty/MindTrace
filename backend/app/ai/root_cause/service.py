import logging
from typing import Dict, Any
from app.ai.root_cause.model_loader import RootCauseModelLoader
from app.ai.root_cause.calibrator import ConfidenceCalibrator
from app.ai.root_cause.feature_builder import RootCauseFeatureBuilder
from app.ai.root_cause.schemas import RootCausePredictionRequest, RootCausePredictionResponse

logger = logging.getLogger("mindtrace.ai.root_cause.service")

class RootCauseService:
    def __init__(self):
        self.model, self.classes, self.model_metadata = RootCauseModelLoader.load_root_cause_model()
        self.calibrator_model, self.calibrator_metadata = RootCauseModelLoader.load_calibrator_model()
        self.feature_builder = RootCauseFeatureBuilder()
        self.calibrator = ConfidenceCalibrator(self.calibrator_model, self.calibrator_metadata)

    def predict_root_cause(self, request: RootCausePredictionRequest) -> RootCausePredictionResponse:
        # Step 1: Build pandas DataFrame feature row
        df_features = self.feature_builder.build_features(request)

        # Step 2: Predict raw probabilities with Root Cause Model V1
        raw_probabilities_array = self.model.predict_proba(df_features)[0]
        predicted_class_idx = int(raw_probabilities_array.argmax())
        predicted_root_cause = str(self.classes[predicted_class_idx])
        raw_prob_dict = {
            cls: float(raw_probabilities_array[i])
            for i, cls in enumerate(self.classes)
        }
        raw_predicted_confidence = float(raw_probabilities_array[predicted_class_idx])

        # Step 3: Calibrate probabilities
        calibrated_prob_dict, calibrated_predicted_confidence = self.calibrator.calibrate(
            raw_probabilities_array,
            self.classes,
            predicted_root_cause
        )

        return RootCausePredictionResponse(
            root_cause=predicted_root_cause,
            calibrated_probability=round(calibrated_predicted_confidence, 4),
            raw_probability=round(raw_predicted_confidence, 4),
            calibrated_probabilities={k: round(v, 4) for k, v in calibrated_prob_dict.items()},
            raw_probabilities={k: round(v, 4) for k, v in raw_prob_dict.items()},
            subject=request.subject,
            calibration_method=self.calibrator.method_name
        )

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "root_cause_model": self.model_metadata,
            "confidence_calibrator": self.calibrator_metadata
        }

_root_cause_service_instance = None

def get_root_cause_service() -> RootCauseService:
    global _root_cause_service_instance
    if _root_cause_service_instance is None:
        _root_cause_service_instance = RootCauseService()
    return _root_cause_service_instance
