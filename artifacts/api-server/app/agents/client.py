import os
from google import genai
from google.genai import types


def _build_client() -> genai.Client:
    gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
    proxy_api_key = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY", "")
    proxy_base_url = os.environ.get("AI_INTEGRATIONS_GEMINI_BASE_URL", "")

    if gemini_api_key:
        return genai.Client(api_key=gemini_api_key)

    if proxy_api_key and proxy_base_url:
        return genai.Client(
            api_key=proxy_api_key,
            http_options=types.HttpOptions(
                base_url=proxy_base_url,
                api_version="",
            ),
        )

    raise RuntimeError(
        "No Gemini credentials found. Set GEMINI_API_KEY (for Cloud Run / production) "
        "or both AI_INTEGRATIONS_GEMINI_API_KEY and AI_INTEGRATIONS_GEMINI_BASE_URL "
        "(for Replit development)."
    )


gemini_client: genai.Client = _build_client()

MODEL = "gemini-2.5-flash"
