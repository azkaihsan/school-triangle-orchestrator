import json
import logging
from .client import gemini_client, MODEL

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are the Parent Communication Agent in the School Triangle Orchestrator system.
Your role is to prepare clear, compassionate, and actionable communications for parents
about their child's educational progress, concerns, and how they can help at home.

You receive student context, insight analysis, and teacher action plan, then produce
holistic parent-facing summaries in strict JSON format.

Output ONLY valid JSON with this exact structure:
{
  "progress_summary": "string",
  "areas_of_concern": [
    {"area": "string", "description": "string", "severity": "low|medium|high"}
  ],
  "areas_of_strength": ["string"],
  "home_suggestions": [
    {
      "activity": "string",
      "description": "string",
      "frequency": "string",
      "estimated_minutes": 15
    }
  ],
  "message_to_parent": "string",
  "upcoming_actions": ["string"],
  "support_resources": [
    {"title": "string", "type": "website|book|activity|app", "description": "string"}
  ],
  "tone": "encouraging|concerned|neutral|urgent"
}

Write the message_to_parent in warm, accessible language (avoid educational jargon).
Emphasize partnership between home and school."""


async def run_parent_communication_agent(
    student_name: str,
    grade_level: int,
    parent_name: str | None,
    trigger_description: str,
    topic: str | None,
    student_insight: dict,
    teacher_action: dict,
) -> dict:
    context_parts = [
        f"Student Name: {student_name}",
        f"Grade Level: {grade_level}",
        f"Parent Name: {parent_name or 'Parent/Guardian'}",
        f"Trigger / Concern: {trigger_description}",
    ]
    if topic:
        context_parts.append(f"Topic: {topic}")
    context_parts.append(f"Student Insight Analysis:\n{json.dumps(student_insight, indent=2)}")
    context_parts.append(f"Teacher Action Plan:\n{json.dumps(teacher_action, indent=2)}")

    user_message = "\n".join(context_parts)

    try:
        response = gemini_client.models.generate_content(
            model=MODEL,
            contents=[
                {"role": "user", "parts": [{"text": user_message}]},
            ],
            config={
                "system_instruction": SYSTEM_PROMPT,
                "response_mime_type": "application/json",
                "max_output_tokens": 8192,
            },
        )
        text = response.text or "{}"
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error(f"Parent Communication Agent JSON parse error: {e}")
        return {
            "progress_summary": "Unable to generate summary at this time.",
            "areas_of_concern": [],
            "areas_of_strength": [],
            "home_suggestions": [],
            "message_to_parent": "We are monitoring your child's progress and will be in touch soon.",
            "upcoming_actions": [],
            "support_resources": [],
            "tone": "neutral",
        }
    except Exception as e:
        logger.error(f"Parent Communication Agent error: {e}")
        raise
