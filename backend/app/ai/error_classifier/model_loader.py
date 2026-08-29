import logging
import joblib
from pathlib import Path
from typing import Dict, Any, Tuple
from app.core.config import settings

logger = logging.getLogger("mindtrace.error_classifier.model_loader")

class ErrorClassifierModelLoader:
    _instance = None
    _vectorizer = None
    _classifier = None
    _classes = None
    _metadata: Dict[str, Any] = {}
    _loaded = False

    @classmethod
    def load_model(cls, model_path: str = None) -> Tuple[Any, Any, Any, Dict[str, Any]]:
        if cls._loaded:
            return cls._vectorizer, cls._classifier, cls._classes, cls._metadata

        if not model_path:
            model_path = getattr(settings, "ERROR_CLASSIFIER_PATH", "backend/models/mindtrace_error_classifier.joblib")

        path = Path(model_path)
        if not path.is_absolute():
            # Resolve relative to backend directory or workspace root
            curr_dir = Path(__file__).resolve().parent
            # Check relative to backend dir
            backend_dir = Path(__file__).resolve().parents[3]
            repo_root = backend_dir.parent if backend_dir.name == "backend" else backend_dir
            
            p1 = repo_root / model_path
            p2 = backend_dir / model_path
            p3 = repo_root / "mindtrace_error_classifier.joblib"
            p4 = repo_root / "models" / "mindtrace_error_classifier.joblib"
            p5 = repo_root / "backend" / "models" / "mindtrace_error_classifier.joblib"

            for candidate in [p1, p2, p3, p4, p5]:
                if candidate.exists():
                    path = candidate
                    break

        if not path.exists():
            logger.error(f"Error Classifier model file not found at: {path}")
            raise FileNotFoundError(f"Error Classifier model joblib file not found at {path}")

        try:
            logger.info(f"Loading Error Classifier model from {path}...")
            model_bundle = joblib.load(path)

            if isinstance(model_bundle, dict):
                cls._vectorizer = model_bundle.get("vectorizer")
                cls._classifier = model_bundle.get("classifier")
                cls._classes = model_bundle.get("classes")
                cls._metadata = {
                    "model_name": model_bundle.get("model_name", "MindTrace Error Classifier"),
                    "version": model_bundle.get("version", "1.0.0"),
                    "algorithm": model_bundle.get("algorithm", "TF-IDF + Logistic Regression"),
                    "dataset": model_bundle.get("dataset", "MAP"),
                    "evaluation_metrics": model_bundle.get("evaluation_metrics", {})
                }
            else:
                # Direct model object or tuple
                cls._classifier = model_bundle
                cls._vectorizer = getattr(model_bundle, "vectorizer", None)
                cls._classes = getattr(model_bundle, "classes_", [])
                cls._metadata = {
                    "model_name": "MindTrace Error Classifier",
                    "version": "1.0.0",
                    "algorithm": "TF-IDF + Logistic Regression",
                    "dataset": "MAP"
                }

            if cls._classes is not None and hasattr(cls._classes, "tolist"):
                cls._classes = cls._classes.tolist()

            cls._loaded = True
            logger.info(f"Error Classifier model loaded successfully. Version: {cls._metadata.get('version')}")
            return cls._vectorizer, cls._classifier, cls._classes, cls._metadata
        except Exception as e:
            logger.error(f"Failed to load Error Classifier model from {path}: {str(e)}", exc_info=True)
            raise RuntimeError(f"Could not load Error Classifier model: {str(e)}") from e

    @classmethod
    def get_metadata(cls) -> Dict[str, Any]:
        if not cls._loaded:
            cls.load_model()
        return cls._metadata
