from datetime import datetime
from typing import Any
from pydantic import BaseModel, EmailStr, field_validator


class HealthResponse(BaseModel):
    status: str


class TeacherOut(BaseModel):
    id: int
    name: str
    email: str
    subject_area: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ParentOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class StudentCreate(BaseModel):
    name: str
    grade_level: int
    teacher_id: int | None = None
    parent_id: int | None = None
    learning_style: str | None = None
    notes: str | None = None


class StudentUpdate(BaseModel):
    name: str | None = None
    grade_level: int | None = None
    teacher_id: int | None = None
    parent_id: int | None = None
    learning_style: str | None = None
    notes: str | None = None


class StudentOut(BaseModel):
    id: int
    name: str
    grade_level: int
    teacher_id: int | None
    parent_id: int | None
    learning_style: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
    teacher: TeacherOut | None = None
    parent: ParentOut | None = None

    model_config = {"from_attributes": True}


class StudentListOut(BaseModel):
    id: int
    name: str
    grade_level: int
    learning_style: str | None
    teacher_id: int | None
    parent_id: int | None
    created_at: datetime

    model_config = {"from_attributes": True}


class InterventionOut(BaseModel):
    id: int
    student_id: int
    topic_id: int | None
    type: str
    title: str
    description: str | None
    status: str
    ai_analysis: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AssignmentOut(BaseModel):
    id: int
    student_id: int
    topic_id: int | None
    title: str
    description: str | None
    due_date: str | None
    status: str
    created_by_agent: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ParentNotificationOut(BaseModel):
    id: int
    student_id: int
    parent_id: int | None
    message: str
    type: str
    channel: str
    status: str
    ai_content: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}


class OrchestrationLogOut(BaseModel):
    id: int
    student_id: int
    trigger_description: str
    topic: str | None
    student_insight_result: dict | None
    teacher_action_result: dict | None
    parent_communication_result: dict | None
    scheduling_result: dict | None
    unified_response: dict | None
    status: str
    execution_time_ms: int | None
    created_at: datetime

    model_config = {"from_attributes": True}


class OrchestrateRequest(BaseModel):
    student_id: int
    trigger_description: str
    topic: str | None = None


class AgentStatus(BaseModel):
    agent: str
    status: str
    error: str | None = None


class OrchestrateResponse(BaseModel):
    orchestration_id: int
    student_id: int
    trigger_description: str
    topic: str | None
    status: str
    execution_time_ms: int
    agent_statuses: list[AgentStatus]
    student_insight: dict
    teacher_action: dict
    parent_communication: dict
    scheduling: dict
    summary: str


class StudentInsightResponse(BaseModel):
    student_id: int
    student_name: str
    analysis: dict
    interventions: list[InterventionOut]


class TeacherActionResponse(BaseModel):
    student_id: int
    student_name: str
    action_plan: dict
    assignments: list[AssignmentOut]
    interventions: list[InterventionOut]


class ParentSummaryResponse(BaseModel):
    student_id: int
    student_name: str
    parent_name: str | None
    summary: dict
    notifications: list[ParentNotificationOut]


class ScheduleRequest(BaseModel):
    student_id: int
    event_type: str
    title: str
    description: str | None = None
    scheduled_date: str | None = None
    participants: list[str] = []


class ScheduleResponse(BaseModel):
    status: str
    mcp_tool_calls: list[dict]
    calendar_events: list[dict]
    tasks_created: list[dict]
    reminders_set: list[dict]
    summary: str
