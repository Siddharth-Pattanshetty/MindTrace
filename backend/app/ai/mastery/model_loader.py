import logging
import joblib
import json
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional

logger = logging.getLogger("mindtrace.ai.mastery.model_loader")

class MasteryModelLoader:
    _mastery_model = None
    _booster = None
    _metadata: Dict[str, Any] = {}

    @classmethod
    def _find_file(cls, relative_or_filename: str) -> Path:
        target = Path(relative_or_filename)
        if target.is_absolute() and target.exists():
            return target

        curr_dir = Path(__file__).resolve().parent
        backend_dir = Path(__file__).resolve().parents[3]
        repo_root = backend_dir.parent if backend_dir.name == "backend" else backend_dir

        candidates = [
            repo_root / relative_or_filename,
            backend_dir / relative_or_filename,
            repo_root / "models" / Path(relative_or_filename).name,
            backend_dir / "models" / Path(relative_or_filename).name,
            repo_root / Path(relative_or_filename).name,
        ]

        for cand in candidates:
            if cand.exists():
                return cand

        raise FileNotFoundError(f"Could not locate required model file '{relative_or_filename}'. Checked: {candidates}")

    @classmethod
    def load_mastery_model(cls) -> Tuple[Any, Any, Dict[str, Any]]:
        if cls._mastery_model is not None and cls._booster is not None:
            return cls._mastery_model, cls._booster, cls._metadata

        model_path = cls._find_file("models/mindtrace_mastery_model.joblib")
        meta_path = cls._find_file("models/mindtrace_mastery_model_metadata.json")

        logger.info(f"Loading Mastery Model from {model_path}...")
        cls._mastery_model = joblib.load(model_path)

        if hasattr(cls._mastery_model, "get_booster"):
            cls._booster = cls._mastery_model.get_booster()
        else:
            cls._booster = cls._mastery_model

        if meta_path.exists():
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    cls._metadata = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load Mastery metadata JSON: {e}")
                cls._metadata = {}

        if not cls._metadata:
            cls._metadata = {
                "model_name": "MindTrace Mastery Predictor",
                "version": "1.0.0",
                "algorithm": "XGBoost",
                "dataset": "ASSISTments Skill Builder"
            }

        logger.info("Mastery Model loaded successfully.")
        return cls._mastery_model, cls._booster, cls._metadata
