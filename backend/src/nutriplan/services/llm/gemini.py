"""
Gemini client helper for structured JSON generation.
"""

from json import JSONDecodeError, loads

from google.genai import Client
from google.genai.types import GenerateContentConfig


class GeminiClient:
    """
    Interface to interact with Gemini's LLM service.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gemini-2.5-pro",
        temperature: float = 0.4,
    ) -> None:
        """
        Initializes the Gemini LLM service.

        Args:
            api_key:     API key for Gemini.
            model:       Name of Gemini model to use.
            temperature: Temperature for response generation, controlling randomness.

        Raises:
            RuntimeError: If API key isn't provided and 'GOOGLE_API_KEY' is not set.

        """

        self.client = Client(api_key=api_key) if api_key else Client()
        self.model = model
        self.temperature = temperature

    def generate_json(self, prompt: str) -> dict:
        """
        Generate structured JSON via response_mime_type="application/json".
        """

        resp = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=GenerateContentConfig(
                response_mime_type="application/json",
                temperature=self.temperature,
            ),
        )

        text = resp.text or ""
        try:
            return loads(text)
        except JSONDecodeError as e:
            start = min(
                [p for p in (text.find("{"), text.find("[")) if p != -1], default=-1
            )

            end = max(text.rfind("}"), text.rfind("]"))
            if start != -1 and end != -1 and end > start:
                return loads(text[start : end + 1])

            msg = f"Gemini did not return valid JSON: {e}\n{text}"
            raise RuntimeError(msg) from e
