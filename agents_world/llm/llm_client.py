import requests
import json
import time
from typing import Dict, Any
from agents_world.utils.logger import logger
from agents_world.utils.helpers import Config

class LLMUnavailableError(Exception):
    pass

class LLMClient:
    """Wrapper for Ollama HTTP API."""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMClient, cls).__new__(cls)
            cls._instance.config = Config()
            cls._instance.base_url = cls._instance.config.get("llm.base_url", "http://localhost:11434")
            cls._instance.model = cls._instance.config.get("llm.model_name", "mistral")
            cls._instance.timeout = cls._instance.config.get("llm.timeout", 30)
            cls._instance.max_retries = cls._instance.config.get("llm.max_retries", 3)
        return cls._instance
        
    def complete(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Standard LLM completion."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature
            }
        }
        return self._send_request(payload)

    def complete_structured(self, prompt: str, schema: dict) -> Dict[str, Any]:
        """Structured LLM completion instructing JSON format."""
        prompt_with_schema = f"{prompt}\n\nPlease respond strictly in JSON matching this schema:\n{json.dumps(schema)}"
        payload = {
            "model": self.model,
            "prompt": prompt_with_schema,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.2
            }
        }
        response_text = self._send_request(payload)
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON from LLM: {response_text}")
            return {}

    def _send_request(self, payload: dict) -> str:
        """Helper to send request with retries."""
        delays = [1, 2, 4]
        for attempt in range(self.max_retries):
            try:
                response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=self.timeout)
                response.raise_for_status()
                result = response.json()
                return result.get("response", "").strip()
            except requests.RequestException as e:
                logger.warning(f"LLM request failed (attempt {attempt+1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(delays[attempt])
                else:
                    logger.error("LLM unavailable after max retries.")
                    raise LLMUnavailableError("Could not reach LLM backend")
        return ""
