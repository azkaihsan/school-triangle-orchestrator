from datetime import datetime, timezone
from sqlalchemy import (
    Integer, String, Text, DateTime, ForeignKey, JSON, Enum as SAEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    subject_area: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    students: Mapped[list["Student"]] = relationship("Student", back_populates="teacher")


class Parent(Base):
    __tablename__ = "parents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    students: Mapped[list["Student"]] = relationship("Student", back_populates="parent")
    notifications: Mapped[list["ParentNotification"]] = relationship("ParentNotification", back_populates="parent")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    grade_level: Mapped[int] = mapped_column(Integer, nullable=False)
    teacher_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("teachers.id"), nullable=True)
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("parents.id"), nullable=True)
    learning_style: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    teacher: Mapped["Teacher | None"] = relationship("Teacher", back_populates="students")
    parent: Mapped["Parent | None"] = relationship("Parent", back_populates="students")
    interventions: Mapped[list["Intervention"]] = relationship("Intervention", back_populates="student")
    assignments: Mapped[list["Assignment"]] = relationship("Assignment", back_populates="student")
    notifications: Mapped[list["ParentNotification"]] = relationship("ParentNotification", back_populates="student")
    orchestration_logs: Mapped[list["OrchestrationLog"]] = relationship("OrchestrationLog", back_populates="student")


class CurriculumTopic(Base):
    __tablename__ = "curriculum_topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    subject: Mapped[str] = mapped_column(String(100), nullable=False)
    topic_name: Mapped[str] = mapped_column(String(255), nullable=False)
    grade_level: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    learning_objectives: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    interventions: Mapped[list["Intervention"]] = relationship("Intervention", back_populates="topic")
    assignments: Mapped[list["Assignment"]] = relationship("Assignment", back_populates="topic")


class Intervention(Base):
    __tablename__ = "interventions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False)
    topic_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("curriculum_topics.id"), nullable=True)
    type: Mapped[str] = mapped_column(
        SAEnum("remediation", "enrichment", "review", "assessment", name="intervention_type"),
        nullable=False,
        default="remediation"
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        SAEnum("pending", "active", "completed", "cancelled", name="intervention_status"),
        nullable=False,
        default="pending"
    )
    ai_analysis: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    student: Mapped["Student"] = relationship("Student", back_populates="interventions")
    topic: Mapped["CurriculumTopic | None"] = relationship("CurriculumTopic", back_populates="interventions")


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False)
    topic_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("curriculum_topics.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    due_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(
        SAEnum("assigned", "in_progress", "completed", "overdue", name="assignment_status"),
        nullable=False,
        default="assigned"
    )
    created_by_agent: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    student: Mapped["Student"] = relationship("Student", back_populates="assignments")
    topic: Mapped["CurriculumTopic | None"] = relationship("CurriculumTopic", back_populates="assignments")


class ParentNotification(Base):
    __tablename__ = "parent_notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("parents.id"), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(
        SAEnum("progress_update", "concern_alert", "achievement", "meeting_request", name="notification_type"),
        nullable=False,
        default="progress_update"
    )
    channel: Mapped[str] = mapped_column(
        SAEnum("email", "sms", "app", name="notification_channel"),
        nullable=False,
        default="email"
    )
    status: Mapped[str] = mapped_column(
        SAEnum("pending", "sent", "read", name="notification_status"),
        nullable=False,
        default="pending"
    )
    ai_content: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    student: Mapped["Student"] = relationship("Student", back_populates="notifications")
    parent: Mapped["Parent | None"] = relationship("Parent", back_populates="notifications")


class OrchestrationLog(Base):
    __tablename__ = "orchestration_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False)
    trigger_description: Mapped[str] = mapped_column(Text, nullable=False)
    topic: Mapped[str | None] = mapped_column(String(255), nullable=True)
    student_insight_result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    teacher_action_result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    parent_communication_result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    scheduling_result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    unified_response: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(
        SAEnum("success", "partial", "failed", name="orchestration_status"),
        nullable=False,
        default="success"
    )
    execution_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    student: Mapped["Student"] = relationship("Student", back_populates="orchestration_logs")
