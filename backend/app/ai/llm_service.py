import json
import logging
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    """
    Unified LLM Provider Abstraction Layer for MindTrace.
    Supports LatentCode, OpenAI, and Rule-Based Deterministic Fallback.
    """
    
    def __init__(self):
        self.latentcode_url = getattr(settings, "LATENTCODE_LLM_URL", None)
        self.latentcode_key = getattr(settings, "LATENTCODE_API_KEY", None)
        self.openai_key = getattr(settings, "OPENAI_API_KEY", None)
        self.timeout = 10.0 # seconds

    def _get_active_provider(self) -> str:
        if self.latentcode_url and self.latentcode_url.strip():
            return "LATENTCODE"
        elif self.openai_key and self.openai_key.strip():
            return "OPENAI"
        return "FALLBACK"

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        provider = self._get_active_provider()
        
        if provider == "LATENTCODE":
            return self._call_latentcode(prompt, system_prompt)
        elif provider == "OPENAI":
            return self._call_openai(prompt, system_prompt)
        else:
            return self._fallback_generate(prompt)

    def generate_structured(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        res_text = self.generate(prompt, system_prompt)
        try:
            # Strip markdown code fencing if present
            cleaned = res_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            return json.loads(cleaned.strip())
        except Exception as e:
            logger.warning(f"Failed to parse JSON response from LLM, returning raw text structure: {e}")
            return {"raw_response": res_text}

    def _call_latentcode(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        headers = {"Content-Type": "application/json"}
        if self.latentcode_key:
            headers["Authorization"] = f"Bearer {self.latentcode_key}"

        payload = {
            "model": "latentcode-agent",
            "messages": [
                {"role": "system", "content": system_prompt or "You are MindTrace Diagnostic AI."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        url = self.latentcode_url.rstrip('/')
        if not url.endswith('/chat/completions') and not url.endswith('/generate'):
            url = f"{url}/chat/completions"

        for attempt in range(2):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    resp = client.post(url, headers=headers, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        if "choices" in data and len(data["choices"]) > 0:
                            return data["choices"][0]["message"]["content"]
                        elif "response" in data:
                            return data["response"]
            except Exception as e:
                logger.error(f"LatentCode API attempt {attempt+1} failed: {e}")

        logger.warning("LatentCode provider failed after retries. Reverting to rule-based fallback.")
        return self._fallback_generate(prompt)

    def _call_openai(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_key}"
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt or "You are MindTrace Diagnostic AI."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        for attempt in range(2):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    resp = client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                    if resp.status_code == 200:
                        return resp.json()["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"OpenAI API attempt {attempt+1} failed: {e}")

        return self._fallback_generate(prompt)

    def _fallback_generate(self, prompt: str) -> str:
        """Deterministic rule-based response generator when external APIs are unconfigured."""
        prompt_lower = prompt.lower()
        
        if "explain" in prompt_lower or "root cause" in prompt_lower:
            return json.dumps({
                "explanation": "Sign errors during expansion caused algebraic transposition failures.",
                "remediation_focus": "Algebraic Manipulation & Bracket Expansion"
            })
        elif "practice" in prompt_lower or "question" in prompt_lower:
            return json.dumps({
                "question": "Simplify the expression: 3(x + 4) - 2(x - 1)",
                "expected_answer": "x + 14",
                "explanation": "Expand brackets and collect like terms."
            })
            
        return "MindTrace Rule-Based Diagnostic Analysis: Prerequisite weakness in algebraic manipulation identified."

llm_service = LLMService()
