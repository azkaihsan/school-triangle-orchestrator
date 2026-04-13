import json
import logging
from .client import gemini_client, MODEL

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are the Teacher Action Agent in the School Triangle Orchestrator system.
Your role is to generate targeted intervention plans, curriculum adjustments, and specific assignments
for a teacher to address a student's learning gaps.

You receive student context and insight analysis from the Student Insight Agent, and produce
actionable teacher directives in strict JSON format.

Output ONLY valid JSON with this exact structure:
{
  "intervention_plan": {
    "title": "string",
    "type": "remediation|enrichment|review|assessment",
    "description": "string",
    "duration_weeks": 1,
    "session_frequency": "string",
    "approach": "string"
  },
  "assignments": [
    {
      "title": "string",
      "description": "string",
      "due_in_days": 7,
      "type": "practice|project|quiz|reading",
      "estimated_minutes": 30
    }
  ],
  "curriculum_adjustments": [
    {"area": "string", "adjustment": "string", "rationale": "string"}
  ],
  "teaching_strategies": ["string"],
  "action_summary": "string",
  "priority": "low|medium|high|urgent"
}

Be specific, practical, and aligned to the student's grade level and identified gaps."""


async def run_teacher_action_agent(
    student_name: str,
    grade_level: int,
    trigger_description: str,
    topic: str | None,
    student_insight: dict,
) -> dict:
    context_parts = [
        f"Student Name: {student_name}",
        f"Grade Level: {grade_level}",
        f"Trigger / Concern: {trigger_description}",
    ]
    if topic:
        context_parts.append(f"Topic: {topic}")
    context_parts.append(f"Student Insight Analysis:\n{json.dumps(student_insight, indent=2)}")

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
        logger.error(f"Teacher Action Agent JSON parse error: {e}")
        return {
            "intervention_plan": {
                "title": "Standard Remediation",
                "type": "remediation",
                "description": "General remediation plan",
                "duration_weeks": 2,
                "session_frequency": "3x per week",
                "approach": "individualized instruction",
            },
            "assignments": [],
            "curriculum_adjustments": [],
            "teaching_strategies": [],
            "action_summary": f"Action plan could not be generated. Error: {str(e)}",
            "priority": "medium",
        }
    except Exception as e:
        logger.error(f"Teacher Action Agent error: {e}")
        raise
