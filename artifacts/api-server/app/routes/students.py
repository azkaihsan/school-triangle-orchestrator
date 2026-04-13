import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..models import Student, Intervention, Assignment, ParentNotification
from ..schemas import (
    StudentCreate,
    StudentUpdate,
    StudentOut,
    StudentListOut,
    StudentInsightResponse,
    TeacherActionResponse,
    ParentSummaryResponse,
    InterventionOut,
    AssignmentOut,
    ParentNotificationOut,
)
from ..agents.student_insight import run_student_insight_agent
from ..agents.teacher_action import run_teacher_action_agent
from ..agents.parent_communication import run_parent_communication_agent

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=list[StudentListOut])
async def list_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).order_by(Student.name))
    return result.scalars().all()


@router.post("", response_model=StudentOut, status_code=201)
async def create_student(body: StudentCreate, db: AsyncSession = Depends(get_db)):
    student = Student(**body.model_dump())
    db.add(student)
    await db.commit()
    result = await db.execute(
        select(Student)
        .options(selectinload(Student.teacher), selectinload(Student.parent))
        .where(Student.id == student.id)
    )
    return result.scalar_one()


@router.get("/{student_id}", response_model=StudentOut)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Student)
        .options(selectinload(Student.teacher), selectinload(Student.parent))
        .where(Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.patch("/{student_id}", response_model=StudentOut)
async def update_student(student_id: int, body: StudentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(student, field, value)
    await db.commit()
    result2 = await db.execute(
        select(Student)
        .options(selectinload(Student.teacher), selectinload(Student.parent))
        .where(Student.id == student_id)
    )
    return result2.scalar_one()


@router.delete("/{student_id}", status_code=204)
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await db.delete(student)
    await db.commit()


@router.get("/{student_id}/insights", response_model=StudentInsightResponse)
async def get_student_insights(student_id: int, topic: str | None = None, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Student)
        .options(selectinload(Student.teacher), selectinload(Student.parent))
        .where(Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    ivs_result = await db.execute(
        select(Intervention).where(Intervention.student_id == student_id).order_by(Intervention.created_at.desc()).limit(5)
    )
    prior = [
        {"type": iv.type, "title": iv.title, "status": iv.status}
        for iv in ivs_result.scalars().all()
    ]

    trigger = topic or (student.notes or "General learning assessment")
    analysis = await run_student_insight_agent(
        student_name=student.name,
        grade_level=student.grade_level,
        learning_style=student.learning_style,
        trigger_description=trigger,
        topic=topic,
        prior_interventions=prior,
    )

    all_ivs = await db.execute(
        select(Intervention).where(Intervention.student_id == student_id).order_by(Intervention.created_at.desc())
    )
    interventions = all_ivs.scalars().all()

    return StudentInsightResponse(
        student_id=student.id,
        student_name=student.name,
        analysis=analysis,
        interventions=[InterventionOut.model_validate(iv) for iv in interventions],
    )


@router.get("/{student_id}/interventions", response_model=TeacherActionResponse)
async def get_student_interventions(student_id: int, topic: str | None = None, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Student)
        .options(selectinload(Student.teacher), selectinload(Student.parent))
        .where(Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    trigger = topic or (student.notes or "General learning assessment")

    insight = await run_student_insight_agent(
        student_name=student.name,
        grade_level=student.grade_level,
        learning_style=student.learning_style,
        trigger_description=trigger,
        topic=topic,
    )
    action = await run_teacher_action_agent(
        student_name=student.name,
        grade_level=student.grade_level,
        trigger_description=trigger,
        topic=topic,
        student_insight=insight,
    )

    ivs_result = await db.execute(
        select(Intervention).where(Intervention.student_id == student_id).order_by(Intervention.created_at.desc())
    )
    assignments_result = await db.execute(
        select(Assignment).where(Assignment.student_id == student_id).order_by(Assignment.created_at.desc())
    )

    return TeacherActionResponse(
        student_id=student.id,
        student_name=student.name,
        action_plan=action,
        assignments=[AssignmentOut.model_validate(a) for a in assignments_result.scalars().all()],
        interventions=[InterventionOut.model_validate(iv) for iv in ivs_result.scalars().all()],
    )


@router.get("/{student_id}/parent-summary", response_model=ParentSummaryResponse)
async def get_parent_summary(student_id: int, topic: str | None = None, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Student)
        .options(selectinload(Student.teacher), selectinload(Student.parent))
        .where(Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    trigger = topic or (student.notes or "General learning assessment")
    parent_name = student.parent.name if student.parent else None

    insight = await run_student_insight_agent(
        student_name=student.name,
        grade_level=student.grade_level,
        learning_style=student.learning_style,
        trigger_description=trigger,
        topic=topic,
    )
    action = await run_teacher_action_agent(
        student_name=student.name,
        grade_level=student.grade_level,
        trigger_description=trigger,
        topic=topic,
        student_insight=insight,
    )
    comm = await run_parent_communication_agent(
        student_name=student.name,
        grade_level=student.grade_level,
        parent_name=parent_name,
        trigger_description=trigger,
        topic=topic,
        student_insight=insight,
        teacher_action=action,
    )

    notifs_result = await db.execute(
        select(ParentNotification)
        .where(ParentNotification.student_id == student_id)
        .order_by(ParentNotification.created_at.desc())
    )

    return ParentSummaryResponse(
        student_id=student.id,
        student_name=student.name,
        parent_name=parent_name,
        summary=comm,
        notifications=[ParentNotificationOut.model_validate(n) for n in notifs_result.scalars().all()],
    )
