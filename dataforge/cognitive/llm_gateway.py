"""
DataForge Universal Zero-Config AI & Cognitive Inhabitation Gateway.
Provides completely automatic, user-transparent LLM and generative reasoning.
Seamlessly cascades through provided API keys, environment credentials, local Ollama, and cloud models.
Includes intelligent fail-fast circuit breakers for sub-second offline fallbacks.
"""
from __future__ import annotations

import os
import json
import random
import urllib.request
import urllib.error
from typing import Any, Optional


class UniversalAIGateway:
    """
    Zero-config AI Gateway with intelligent fail-fast circuit breaker and multi-backend support.
    """

    _instance = None

    def __init__(self):
        self.ollama_endpoint = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self._load_env()
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")
        self._gemini_working: Optional[bool] = None
        self._ollama_working: Optional[bool] = None

    def _load_env(self):
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ[k.strip()] = v.strip().strip('"').strip("'")

    @classmethod
    def get_instance(cls) -> UniversalAIGateway:
        if cls._instance is None:
            cls._instance = UniversalAIGateway()
        return cls._instance

    def generate_chat_response(
        self,
        system_instruction: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500,
        api_key: Optional[str] = None
    ) -> Optional[str]:
        """
        Attempts seamless generation via available backends.
        """
        key_to_use = api_key or self.gemini_key

        # 1. Try Gemini if key is available and not marked broken
        if key_to_use and self._gemini_working is not False:
            try:
                res = self._call_gemini(system_instruction, user_prompt, temperature, key_to_use)
                if res:
                    self._gemini_working = True
                    return res
                else:
                    self._gemini_working = False
            except Exception:
                self._gemini_working = False

        # 2. Try Local Ollama if running and not marked broken
        if self._ollama_working is not False:
            try:
                res = self._call_ollama(system_instruction, user_prompt, temperature)
                if res:
                    self._ollama_working = True
                    return res
                else:
                    self._ollama_working = False
            except Exception:
                self._ollama_working = False

        return None

    def _call_gemini(self, system_instruction: str, user_prompt: str, temperature: float, key: str) -> Optional[str]:
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": f"{system_instruction}\n\n{user_prompt}"}]}
            ],
            "generationConfig": {
                "temperature": temperature
            }
        }
        # Try gemini-2.0-flash
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            # Try Bearer
            url_bearer = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
            req_bearer = urllib.request.Request(
                url_bearer,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {key}"
                }
            )
            with urllib.request.urlopen(req_bearer, timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["candidates"][0]["content"]["parts"][0]["text"]

    def _call_ollama(self, system_instruction: str, user_prompt: str, temperature: float) -> Optional[str]:
        url = f"{self.ollama_endpoint}/api/generate"
        payload = {
            "model": "llama3",
            "system": system_instruction,
            "prompt": user_prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response")
