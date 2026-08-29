import logging
import numpy as np
from typing import Dict, Any, Tuple, List

logger = logging.getLogger("mindtrace.ai.root_cause.calibrator")

class ConfidenceCalibrator:
    """
    Applies multiclass probability calibration (Platt / Logistic Calibration)
    to transform raw Root Cause prediction probabilities into calibrated confidence scores.
    """
    def __init__(self, calibrator_model: Any, metadata: Dict[str, Any]):
        self.calibrator_model = calibrator_model
        self.metadata = metadata
        self.method_name = metadata.get("calibration_method", "Platt / Logistic Calibration (Multinomial)")

    def calibrate(
        self,
        raw_probs: np.ndarray,
        base_classes: List[str],
        predicted_class: str
    ) -> Tuple[Dict[str, float], float]:
        """
        Calibrates a 1D raw probability vector (length N_classes).
        Returns:
            - Dict[class_name, calibrated_probability]
            - Calibrated probability for predicted_class
        """
        try:
            # Reshape 1D vector to 2D array for scikit-learn model predict_proba
            raw_2d = np.array(raw_probs).reshape(1, -1)
            
            # Predict calibrated probabilities
            calib_2d = self.calibrator_model.predict_proba(raw_2d)
            calib_1d = calib_2d[0]

            # Verify probability bounds
            calib_1d = np.clip(calib_1d, 0.0, 1.0)
            prob_sum = np.sum(calib_1d)
            if prob_sum > 0:
                calib_1d = calib_1d / prob_sum

            # Map calibrated probabilities back to base_classes order
            calibrator_classes = getattr(self.calibrator_model, "classes_", base_classes)
            if hasattr(calibrator_classes, "tolist"):
                calibrator_classes = calibrator_classes.tolist()

            calibrated_dict = {}
            for i, cls_name in enumerate(base_classes):
                if cls_name in calibrator_classes:
                    calib_idx = calibrator_classes.index(cls_name)
                    calibrated_dict[cls_name] = float(calib_1d[calib_idx])
                else:
                    calibrated_dict[cls_name] = float(raw_probs[i])

            # Validation checks
            for cls_name, val in calibrated_dict.items():
                if np.isnan(val) or np.isinf(val):
                    logger.error(f"Calibrated value for {cls_name} is NaN or Inf. Falling back to raw probability.")
                    cls_idx = base_classes.index(cls_name)
                    calibrated_dict[cls_name] = float(raw_probs[cls_idx])

            calibrated_predicted_confidence = calibrated_dict.get(
                predicted_class,
                float(raw_probs[base_classes.index(predicted_class)])
            )

            return calibrated_dict, calibrated_predicted_confidence

        except Exception as e:
            logger.error(f"Failed to execute calibration: {e}. Returning raw probabilities.", exc_info=True)
            fallback_dict = {cls_name: float(raw_probs[i]) for i, cls_name in enumerate(base_classes)}
            predicted_idx = base_classes.index(predicted_class)
            return fallback_dict, float(raw_probs[predicted_idx])
