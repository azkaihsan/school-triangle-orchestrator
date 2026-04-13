import os
from google import genai
from google.genai import types


def _build_client() -> genai.Client:
    api_key = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY", "")
    base_url = os.environ.get("AI_INTEGRATIONS_GEMINI_BASE_URL", "")
    if not api_key or not base_url:
        raise RuntimeError(
            "Missing Gemini AI integration environment variables. "
            "Ensure AI_INTEGRATIONS_GEMINI_API_KEY and AI_INTEGRATIONS_GEMINI_BASE_URL are set."
        )
    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            base_url=base_url,
            api_version="",
        ),
    )


gemini_client: genai.Client = _build_client()

MODEL = "gemini-2.5-flash"
