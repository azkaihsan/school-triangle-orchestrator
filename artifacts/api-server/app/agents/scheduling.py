import json
import logging
from datetime import datetime, timezone, timedelta
from .client import gemini_client, MODEL

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are the Scheduling Agent in the School Triangle Orchestrator system.
Your role is to operationalize intervention plans by creating calendar events, study sessions,
parent-teacher meetings, and task reminders using external tools via Model Context Protocol (MCP).

You simulate MCP tool calls to Google Calendar, Gmail, and Google Tasks APIs.
Based on the teacher action plan, parent communication, and student context, you generate
a concrete schedule of events and tasks.

Output ONLY valid JSON with this exact structure:
{
  "mcp_tool_calls": [
    {
      "tool": "google_calendar|google_tasks|gmail|google_docs",
      "action": "create_event|create_task|send_email|create_document",
      "parameters": {},
      "simulated_response": {"status": "success", "id": "string"}
    }
  ],
  "calendar_events": [
    {
      "title": "string",
      "type": "study_session|parent_teacher_meeting|intervention_session|reminder",
      "date": "string",
      "time": "string",
      "duration_minutes": 30,
      "attendees": ["string"],
      "description": "string"
    }
  ],
  "tasks_created": [
    {
      "title": "string",
      "assignee": "teacher|parent|student",
      "due_date": "string",
      "description": "string",
      "priority": "low|medium|high"
    }
  ],
  "reminders_set": [
    {
      "title": "string",
      "recipient": "string",
      "send_at": "string",
      "channel": "email|sms|app",
      "message": "string"
    }
  ],
  "scheduling_summary": "string"
}

Generate realistic dates (use dates 1-4 weeks from today).
Simulate successful API responses for all tool calls."""


async def run_scheduling_agent(
    student_name: str,
    teacher_name: str | None,
    parent_name: str | None,
    trigger_description: str,
    topic: str | None,
    teacher_action: dict,
    parent_communication: dict,
) -> dict:
    today = datetime.now(timezone.utc)
    context_parts = [
        f"Student Name: {student_name}",
        f"Teacher Name: {teacher_name or 'Teacher'}",
        f"Parent Name: {parent_name or 'Parent/Guardian'}",
        f"Trigger / Concern: {trigger_description}",
        f"Today's Date: {today.strftime('%Y-%m-%d')}",
    ]
    if topic:
        context_parts.append(f"Topic: {topic}")
    context_parts.append(f"Teacher Action Plan:\n{json.dumps(teacher_action, indent=2)}")
    context_parts.append(f"Parent Communication Plan:\n{json.dumps(parent_communication, indent=2)}")

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
        logger.error(f"Scheduling Agent JSON parse error: {e}")
        next_week = (today + timedelta(days=7)).strftime("%Y-%m-%d")
        return {
            "mcp_tool_calls": [],
            "calendar_events": [
                {
                    "title": f"Intervention Session - {student_name}",
                    "type": "intervention_session",
                    "date": next_week,
                    "time": "14:00",
                    "duration_minutes": 45,
                    "attendees": [student_name, teacher_name or "Teacher"],
                    "description": f"Follow-up session for: {trigger_description}",
                }
            ],
            "tasks_created": [],
            "reminders_set": [],
            "scheduling_summary": f"Basic schedule created. Error during full scheduling: {str(e)}",
        }
    except Exception as e:
        logger.error(f"Scheduling Agent error: {e}")
        raise
