import json
import logging
from .client import gemini_client, MODEL

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are the Student Insight Agent in the School Triangle Orchestrator system.
Your role is to analyze a student's learning situation and identify specific misconceptions and mastery gaps.

You receive structured data about a student (name, grade level, learning style, trigger description, topic of concern)
and return a detailed analysis in strict JSON format.

Output ONLY valid JSON with this exact structure:
{
  "mastery_level": "low|medium|high",
  "misconceptions": [
    {"concept": "string", "description": "string", "severity": "minor|moderate|critical"}
  ],
  "mastery_gaps": [
    {"skill": "string", "description": "string", "prerequisite_skills": ["string"]}
  ],
  "learning_strengths": ["string"],
  "recommended_learning_modalities": ["string"],
  "analysis_summary": "string",
  "confidence_score": 0.0
}

Be specific, educational, and actionable. Base your analysis on the trigger description and student context."""


async def run_student_insight_agent(
    student_name: str,
    grade_level: int,
    learning_style: str | None,
    trigger_description: str,
    topic: str | None,
    prior_interventions: list[dict] | None = None,
) -> dict:
    context_parts = [
        f"Student Name: {student_name}",
        f"Grade Level: {grade_level}",
        f"Learning Style: {learning_style or 'Not specified'}",
        f"Trigger / Concern: {trigger_description}",
    ]
    if topic:
        context_parts.append(f"Topic of Concern: {topic}")
    if prior_interventions:
        context_parts.append(f"Prior Interventions: {json.dumps(prior_interventions, indent=2)}")

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
        logger.error(f"Student Insight Agent JSON parse error: {e}")
        return {
            "mastery_level": "unknown",
            "misconceptions": [],
            "mastery_gaps": [],
            "learning_strengths": [],
            "recommended_learning_modalities": [],
            "analysis_summary": f"Analysis could not be completed. Error: {str(e)}",
            "confidence_score": 0.0,
        }
    except Exception as e:
        logger.error(f"Student Insight Agent error: {e}")
        raise
