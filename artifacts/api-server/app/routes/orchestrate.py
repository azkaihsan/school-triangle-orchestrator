import logging
import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..models import Student, OrchestrationLog, Intervention, Assignment, ParentNotification
from ..schemas import OrchestrateRequest, OrchestrateResponse, OrchestrationLogOut
from ..agents.student_insight import run_student_insight_agent
from ..agents.teacher_action import run_teacher_action_agent
from ..agents.parent_communication import run_parent_communication_agent
from ..agents.scheduling import run_scheduling_agent

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/orchestrate", tags=["orchestrator"])


@router.post("", response_model=OrchestrateResponse, status_code=201)
async def orchestrate(body: OrchestrateRequest, db: AsyncSession = Depends(get_db)):
    start_ms = int(time.time() * 1000)

    result = await db.execute(
        select(Student)
        .options(selectinload(Student.teacher), selectinload(Student.parent))
        .where(Student.id == body.student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    teacher_name = student.teacher.name if student.teacher else None
    parent_name = student.parent.name if student.parent else None

    logger.info(f"Orchestration started for student_id={body.student_id}, trigger='{body.trigger_description}'")

    student_insight = await run_student_insight_agent(
        student_name=student.name,
        grade_level=student.grade_level,
        learning_style=student.learning_style,
        trigger_description=body.trigger_description,
        topic=body.topic,
    )
    logger.info(f"Student Insight Agent complete for student_id={body.student_id}")

    teacher_action = await run_teacher_action_agent(
        student_name=student.name,
        grade_level=student.grade_level,
        trigger_description=body.trigger_description,
        topic=body.topic,
        student_insight=student_insight,
    )
    logger.info(f"Teacher Action Agent complete for student_id={body.student_id}")

    parent_communication = await run_parent_communication_agent(
        student_name=student.name,
        grade_level=student.grade_level,
        parent_name=parent_name,
        trigger_description=body.trigger_description,
        topic=body.topic,
        student_insight=student_insight,
        teacher_action=teacher_action,
    )
    logger.info(f"Parent Communication Agent complete for student_id={body.student_id}")

    scheduling = await run_scheduling_agent(
        student_name=student.name,
        teacher_name=teacher_name,
        parent_name=parent_name,
        trigger_description=body.trigger_description,
        topic=body.topic,
        teacher_action=teacher_action,
        parent_communication=parent_communication,
    )
    logger.info(f"Scheduling Agent complete for student_id={body.student_id}")

    execution_time_ms = int(time.time() * 1000) - start_ms

    plan = teacher_action.get("intervention_plan", {})
    if plan:
        intervention = Intervention(
            student_id=student.id,
            type=plan.get("type", "remediation"),
            title=plan.get("title", "AI-Generated Intervention"),
            description=plan.get("description"),
            status="pending",
            ai_analysis=student_insight,
        )
        db.add(intervention)

    for a in teacher_action.get("assignments", []):
        assignment = Assignment(
            student_id=student.id,
            title=a.get("title", "Assignment"),
            description=a.get("description"),
            status="assigned",
            created_by_agent=True,
        )
        db.add(assignment)

    comm_content = parent_communication
    msg_to_parent = parent_communication.get("message_to_parent", "")
    if msg_to_parent and student.parent_id:
        notification = ParentNotification(
            student_id=student.id,
            parent_id=student.parent_id,
            message=msg_to_parent,
            type="progress_update",
            channel="email",
            status="pending",
            ai_content=comm_content,
        )
        db.add(notification)

    mastery = student_insight.get("mastery_level", "unknown")
    priority = teacher_action.get("priority", "medium")
    summary = (
        f"Orchestration complete for {student.name} (Grade {student.grade_level}). "
        f"Mastery level: {mastery}. Intervention priority: {priority}. "
        f"Teacher action plan generated. Parent communication prepared. "
        f"{len(scheduling.get('calendar_events', []))} calendar event(s) scheduled. "
        f"Execution time: {execution_time_ms}ms."
    )

    unified = {
        "summary": summary,
        "student_name": student.name,
        "mastery_level": mastery,
        "intervention_priority": priority,
        "actions_taken": {
            "interventions_created": 1 if plan else 0,
            "assignments_created": len(teacher_action.get("assignments", [])),
            "parent_notifications": 1 if msg_to_parent else 0,
            "calendar_events": len(scheduling.get("calendar_events", [])),
            "tasks_created": len(scheduling.get("tasks_created", [])),
        },
        "next_checkpoint": scheduling.get("calendar_events", [{}])[0].get("date") if scheduling.get("calendar_events") else None,
    }

    log = OrchestrationLog(
        student_id=student.id,
        trigger_description=body.trigger_description,
        topic=body.topic,
        student_insight_result=student_insight,
        teacher_action_result=teacher_action,
        parent_communication_result=parent_communication,
        scheduling_result=scheduling,
        unified_response=unified,
        status="success",
        execution_time_ms=execution_time_ms,
    )
    db.add(log)
    await db.commit()

    logger.info(f"Orchestration complete: log_id={log.id}, execution_time_ms={execution_time_ms}")

    return OrchestrateResponse(
        orchestration_id=log.id,
        student_id=student.id,
        trigger_description=body.trigger_description,
        topic=body.topic,
        status="success",
        execution_time_ms=execution_time_ms,
        student_insight=student_insight,
        teacher_action=teacher_action,
        parent_communication=parent_communication,
        scheduling=scheduling,
        summary=summary,
    )


@router.get("/logs", response_model=list[OrchestrationLogOut])
async def get_orchestration_logs(
    student_id: int | None = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    query = select(OrchestrationLog).order_by(OrchestrationLog.created_at.desc()).limit(limit)
    if student_id is not None:
        query = query.where(OrchestrationLog.student_id == student_id)
    result = await db.execute(query)
    return result.scalars().all()
