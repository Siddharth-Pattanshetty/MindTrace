import logging
import joblib
import json
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional
from app.core.config import settings

logger = logging.getLogger("mindtrace.ai.root_cause.model_loader")

class RootCauseModelLoader:
    _loaded = False
    _root_cause_model = None
    _classes: List[str] = []
    _root_cause_metadata: Dict[str, Any] = {}
    _calibrator_model = None
    _calibrator_metadata: Dict[str, Any] = {}

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

        raise FileNotFoundError(f"Could not locate required model file '{relative_or_filename}'. Candidate paths checked: {candidates}")

    @classmethod
    def load_root_cause_model(cls) -> Tuple[Any, List[str], Dict[str, Any]]:
        if cls._root_cause_model is not None:
            return cls._root_cause_model, cls._classes, cls._root_cause_metadata

        model_path = cls._find_file("models/mindtrace_root_cause_model.joblib")
        meta_path = cls._find_file("models/mindtrace_root_cause_model_metadata.json")

        logger.info(f"Loading Root Cause Model from {model_path}...")
        cls._root_cause_model = joblib.load(model_path)

        if hasattr(cls._root_cause_model, "classes_"):
            cls._classes = [str(c) for c in cls._root_cause_model.classes_]

        if meta_path.exists():
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    cls._root_cause_metadata = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load Root Cause metadata JSON: {e}")
                cls._root_cause_metadata = {}

        if not cls._root_cause_metadata:
            cls._root_cause_metadata = {
                "model_name": "MindTrace Root Cause Model",
                "version": "1.0.0",
                "algorithm": "Random Forest Pipeline",
                "classes": cls._classes
            }

        logger.info(f"Root Cause Model loaded successfully with {len(cls._classes)} target classes.")
        return cls._root_cause_model, cls._classes, cls._root_cause_metadata

    @classmethod
    def load_calibrator_model(cls) -> Tuple[Any, Dict[str, Any]]:
        if cls._calibrator_model is not None:
            return cls._calibrator_model, cls._calibrator_metadata

        calib_path = cls._find_file("models/mindtrace_confidence_calibrator.joblib")
        meta_path = cls._find_file("models/mindtrace_confidence_calibrator_metadata.json")

        logger.info(f"Loading Confidence Calibrator from {calib_path}...")
        cls._calibrator_model = joblib.load(calib_path)

        if meta_path.exists():
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    cls._calibrator_metadata = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load Calibrator metadata JSON: {e}")
                cls._calibrator_metadata = {}

        if not cls._calibrator_metadata:
            cls._calibrator_metadata = {
                "model_name": "MindTrace Confidence Calibration",
                "version": "1.0.0",
                "calibration_method": "Platt / Logistic Calibration (Multinomial)"
            }

        logger.info("Confidence Calibrator model loaded successfully.")
        return cls._calibrator_model, cls._calibrator_metadata
