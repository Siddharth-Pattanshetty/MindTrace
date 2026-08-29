import numpy as np
import logging
from typing import Tuple, Dict, Any
from app.ai.error_classifier.model_loader import ErrorClassifierModelLoader

logger = logging.getLogger("mindtrace.error_classifier.predictor")

class ErrorClassifierPredictor:
    def __init__(self):
        self.vectorizer, self.classifier, self.classes, self.metadata = ErrorClassifierModelLoader.load_model()

    def format_input(self, question: str, student_answer: str, work_evidence: str = "") -> str:
        """
        Formats text using the exact prompt format used during model training:
        
        [QUESTION]
        {question}

        [STUDENT ANSWER]
        {student_answer}

        [STUDENT EXPLANATION]
        {work_evidence}
        """
        evidence_str = work_evidence if work_evidence else ""
        return f"[QUESTION]\n{question}\n\n[STUDENT ANSWER]\n{student_answer}\n\n[STUDENT EXPLANATION]\n{evidence_str}"

    def predict(self, question: str, student_answer: str, work_evidence: str = "") -> Tuple[str, float]:
        formatted_text = self.format_input(question, student_answer, work_evidence)

        if self.vectorizer is not None:
            features = self.vectorizer.transform([formatted_text])
        else:
            features = [formatted_text]

        if hasattr(self.classifier, "predict_proba"):
            probabilities = self.classifier.predict_proba(features)[0]
            max_idx = np.argmax(probabilities)
            confidence = float(probabilities[max_idx])
            
            if self.classes and max_idx < len(self.classes):
                predicted_class = str(self.classes[max_idx])
            elif hasattr(self.classifier, "classes_"):
                predicted_class = str(self.classifier.classes_[max_idx])
            else:
                predicted_class = str(self.classifier.predict(features)[0])
        else:
            predicted_class = str(self.classifier.predict(features)[0])
            confidence = 1.0

        logger.debug(f"Error classification: {predicted_class} (confidence: {confidence:.4f})")
        return predicted_class, confidence
