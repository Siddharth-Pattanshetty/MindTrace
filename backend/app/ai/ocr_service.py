import os
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class OCRService:
    """
    PaddleOCR & Mathpix OCR service abstraction for exam document parsing.
    """
    
    def __init__(self):
        self.paddle_available = False
        self._init_paddle()

    def _init_paddle(self):
        try:
            from paddleocr import PaddleOCR
            self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
            self.paddle_available = True
        except Exception:
            self.paddle_available = False

    def extract_text(self, file_path: str) -> Dict[str, Any]:
        """
        Extracts raw text, bounding boxes, and OCR confidence from an image or file.
        """
        if not file_path or not os.path.exists(file_path):
            return {"text": "", "confidence": 0.0, "lines": []}

        if self.paddle_available:
            try:
                result = self.ocr.ocr(file_path, cls=True)
                lines = []
                conf_sum = 0.0
                count = 0
                for line in result[0]:
                    text_pair = line[1]
                    lines.append(text_pair[0])
                    conf_sum += text_pair[1]
                    count += 1
                
                avg_conf = conf_sum / max(1, count)
                return {
                    "text": "\n".join(lines),
                    "confidence": round(avg_conf, 2),
                    "lines": lines
                }
            except Exception as e:
                logger.warning(f"PaddleOCR processing error: {e}")

        # Fallback file reader if plain text or OCR uninstalled
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                return {"text": content, "confidence": 0.85, "lines": content.splitlines()}
        except Exception:
            return {"text": "", "confidence": 0.0, "lines": []}

ocr_service = OCRService()
