import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..models import Student
from ..schemas import ScheduleRequest, ScheduleResponse
from ..agents.scheduling import run_scheduling_agent
from ..agents.student_insight import run_student_insight_agent
from ..agents.teacher_action import run_teacher_action_agent
from ..agents.parent_communication import run_parent_communication_agent

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/schedule", tags=["scheduling"])


@router.post("", response_model=ScheduleResponse)
async def create_schedule(body: ScheduleRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Student)
        .options(selectinload(Student.teacher), selectinload(Student.parent))
        .where(Student.id == body.student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    trigger = body.description or f"Scheduling request: {body.title}"
    parent_name = student.parent.name if student.parent else None
    teacher_name = student.teacher.name if student.teacher else None

    insight = await run_student_insight_agent(
        student_name=student.name,
        grade_level=student.grade_level,
        learning_style=student.learning_style,
        trigger_description=trigger,
        topic=None,
    )
    action = await run_teacher_action_agent(
        student_name=student.name,
        grade_level=student.grade_level,
        trigger_description=trigger,
        topic=None,
        student_insight=insight,
    )
    comm = await run_parent_communication_agent(
        student_name=student.name,
        grade_level=student.grade_level,
        parent_name=parent_name,
        trigger_description=trigger,
        topic=None,
        student_insight=insight,
        teacher_action=action,
    )
    schedule = await run_scheduling_agent(
        student_name=student.name,
        teacher_name=teacher_name,
        parent_name=parent_name,
        trigger_description=trigger,
        topic=None,
        teacher_action=action,
        parent_communication=comm,
    )

    return ScheduleResponse(
        status="scheduled",
        mcp_tool_calls=schedule.get("mcp_tool_calls", []),
        calendar_events=schedule.get("calendar_events", []),
        tasks_created=schedule.get("tasks_created", []),
        reminders_set=schedule.get("reminders_set", []),
        summary=schedule.get("scheduling_summary", ""),
    )
