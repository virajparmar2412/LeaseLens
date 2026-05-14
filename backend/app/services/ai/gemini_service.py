import json

from app.ai.gemini_client import get_gemini_client
from app.core.config import settings


class GeminiService:
    def __init__(self) -> None:
        self.client = get_gemini_client()
        self.model = settings.gemini_model

    def is_enabled(self) -> bool:
        return self.client is not None

    def generate_recommendation_explanation(self, context: dict) -> str | None:
        if not self.client:
            return None

        prompt = (
            "You are LeaseLens, an enterprise rental pricing copilot. "
            "Write a concise pricing explanation for a real estate analyst. "
            "Explain the main drivers of the recommendation, confidence level, "
            "and neighborhood context in 3 to 5 sentences.\n\n"
            f"Context:\n{json.dumps(context)}"
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text.strip() if response.text else None

    def interpret_feedback(self, feedback_text: str, context: dict) -> dict | None:
        if not self.client:
            return None

        prompt = (
            "You are converting analyst pricing feedback into a structured action plan. "
            "Return valid JSON only with keys: parsed_intent, pricing_adjustment, "
            "comparable_actions, explanation. comparable_actions must be an array of "
            "objects with comparable_id and action. Keep pricing_adjustment numeric.\n\n"
            f"Feedback:\n{feedback_text}\n\n"
            f"Context:\n{json.dumps(context)}"
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
        if not response.text:
            return None
        try:
            parsed = json.loads(response.text)
        except json.JSONDecodeError:
            return None

        if not isinstance(parsed, dict):
            return None
        parsed.setdefault("parsed_intent", "manual refinement")
        parsed.setdefault("pricing_adjustment", 0)
        parsed.setdefault("comparable_actions", [])
        parsed.setdefault("explanation", "")
        return parsed
