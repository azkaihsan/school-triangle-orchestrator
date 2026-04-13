import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .models import Teacher, Parent, Student, CurriculumTopic, Intervention, OrchestrationLog

logger = logging.getLogger(__name__)


async def seed_if_empty(db: AsyncSession) -> None:
    count_result = await db.execute(select(func.count()).select_from(Student))
    count = count_result.scalar()
    if count and count > 0:
        logger.info("Database already seeded, skipping.")
        return

    logger.info("Seeding database with sample data...")

    teachers = [
        Teacher(name="Ms. Anita Rahmawati", email="a.rahmawati@school.edu", subject_area="Mathematics"),
        Teacher(name="Mr. Budi Santoso", email="b.santoso@school.edu", subject_area="Science"),
    ]
    for t in teachers:
        db.add(t)
    await db.flush()

    parents = [
        Parent(name="Ibu Sari Dewi", email="sari.dewi@email.com", phone="+62-812-0001-0001"),
        Parent(name="Pak Hendra Wijaya", email="h.wijaya@email.com", phone="+62-812-0002-0002"),
        Parent(name="Ibu Lestari Nugroho", email="lestari.n@email.com", phone="+62-812-0003-0003"),
    ]
    for p in parents:
        db.add(p)
    await db.flush()

    students = [
        Student(
            name="Dinda Permata",
            grade_level=5,
            teacher_id=teachers[0].id,
            parent_id=parents[0].id,
            learning_style="visual",
            notes="Struggles with abstract concepts but excels in visual representations. "
                  "Has been having difficulty with fractions this semester.",
        ),
        Student(
            name="Rizky Pratama",
            grade_level=5,
            teacher_id=teachers[0].id,
            parent_id=parents[1].id,
            learning_style="kinesthetic",
            notes="Active learner, works best with hands-on activities. "
                  "Showing gaps in multiplication and division of fractions.",
        ),
        Student(
            name="Aulia Safitri",
            grade_level=6,
            teacher_id=teachers[1].id,
            parent_id=parents[2].id,
            learning_style="auditory",
            notes="Strong verbal skills. Recently struggling with scientific notation "
                  "and unit conversion in Physics.",
        ),
    ]
    for s in students:
        db.add(s)
    await db.flush()

    topics = [
        CurriculumTopic(
            subject="Mathematics",
            topic_name="Fractions — Adding and Subtracting",
            grade_level=5,
            description="Adding and subtracting fractions with unlike denominators.",
            learning_objectives=[
                "Find common denominators",
                "Add fractions with unlike denominators",
                "Subtract fractions with unlike denominators",
                "Simplify results",
            ],
        ),
        CurriculumTopic(
            subject="Mathematics",
            topic_name="Fractions — Multiplying and Dividing",
            grade_level=5,
            description="Multiplying and dividing fractions and mixed numbers.",
            learning_objectives=[
                "Multiply fractions",
                "Divide fractions using reciprocals",
                "Multiply and divide mixed numbers",
            ],
        ),
        CurriculumTopic(
            subject="Science",
            topic_name="Scientific Notation",
            grade_level=6,
            description="Expressing very large and very small numbers in scientific notation.",
            learning_objectives=[
                "Convert standard form to scientific notation",
                "Convert scientific notation to standard form",
                "Perform operations with numbers in scientific notation",
            ],
        ),
        CurriculumTopic(
            subject="Science",
            topic_name="Unit Conversion and Measurement",
            grade_level=6,
            description="Converting between units in the metric and imperial systems.",
            learning_objectives=[
                "Identify common units of measurement",
                "Convert units within the metric system",
                "Apply dimensional analysis",
            ],
        ),
    ]
    for tp in topics:
        db.add(tp)
    await db.flush()

    interventions = [
        Intervention(
            student_id=students[0].id,
            topic_id=topics[0].id,
            type="remediation",
            title="Fraction Foundation Review — Dinda",
            description="Visual-based remediation using fraction bars and number lines to "
                        "rebuild conceptual understanding of equivalent fractions.",
            status="active",
            ai_analysis={
                "mastery_level": "low",
                "misconceptions": [
                    {
                        "concept": "Equivalent fractions",
                        "description": "Confuses numerator manipulation when finding common denominators",
                        "severity": "critical",
                    }
                ],
                "mastery_gaps": [
                    {
                        "skill": "Finding common denominators",
                        "description": "Cannot reliably identify the LCM of two denominators",
                        "prerequisite_skills": ["multiplication tables", "factors and multiples"],
                    }
                ],
                "analysis_summary": "Student needs visual scaffolding to understand fraction equivalence.",
            },
        ),
        Intervention(
            student_id=students[1].id,
            topic_id=topics[1].id,
            type="remediation",
            title="Fraction Operations Practice — Rizky",
            description="Hands-on activities using physical manipulatives to reinforce "
                        "multiplication and division of fractions.",
            status="pending",
            ai_analysis={
                "mastery_level": "medium",
                "misconceptions": [
                    {
                        "concept": "Dividing fractions",
                        "description": "Does not apply the 'multiply by reciprocal' rule consistently",
                        "severity": "moderate",
                    }
                ],
                "mastery_gaps": [],
                "analysis_summary": "Student has partial understanding; needs procedural consolidation.",
            },
        ),
    ]
    for iv in interventions:
        db.add(iv)
    await db.flush()

    log = OrchestrationLog(
        student_id=students[0].id,
        trigger_description="Dinda failed the fraction quiz with a score of 45%. "
                            "She seems confused about finding common denominators.",
        topic="Fractions — Adding and Subtracting",
        student_insight_result={
            "mastery_level": "low",
            "misconceptions": [
                {
                    "concept": "Common denominators",
                    "description": "Student multiplies numerator incorrectly when scaling denominators",
                    "severity": "critical",
                }
            ],
            "mastery_gaps": [
                {
                    "skill": "LCM computation",
                    "description": "Cannot compute LCM reliably",
                    "prerequisite_skills": ["multiplication facts"],
                }
            ],
            "learning_strengths": ["Visual pattern recognition", "Number line usage"],
            "recommended_learning_modalities": ["visual", "concrete manipulatives"],
            "analysis_summary": "Dinda demonstrates conceptual confusion at the denominator scaling step.",
            "confidence_score": 0.87,
        },
        teacher_action_result={
            "intervention_plan": {
                "title": "Visual Fraction Remediation",
                "type": "remediation",
                "description": "Use fraction strips and visual models to rebuild equivalence concept",
                "duration_weeks": 2,
                "session_frequency": "3x per week, 30 minutes each",
                "approach": "concrete-pictorial-abstract (CPA) method",
            },
            "assignments": [
                {
                    "title": "Fraction Bar Matching Worksheet",
                    "description": "Match fractions that are equivalent using fraction bar diagrams",
                    "due_in_days": 3,
                    "type": "practice",
                    "estimated_minutes": 20,
                }
            ],
            "curriculum_adjustments": [
                {
                    "area": "Pacing",
                    "adjustment": "Slow down fraction unit by 1 week",
                    "rationale": "Ensure conceptual foundation before procedural fluency",
                }
            ],
            "teaching_strategies": ["CPA method", "Peer tutoring", "Visual anchor charts"],
            "action_summary": "Pause abstract procedures; return to concrete fraction models for 2 weeks.",
            "priority": "high",
        },
        parent_communication_result={
            "progress_summary": "Dinda is working on strengthening her fraction skills this month.",
            "areas_of_concern": [
                {
                    "area": "Fractions",
                    "description": "Difficulty finding common denominators when adding/subtracting fractions",
                    "severity": "medium",
                }
            ],
            "areas_of_strength": ["Reading comprehension", "Visual problem-solving"],
            "home_suggestions": [
                {
                    "activity": "Cooking fractions",
                    "description": "Involve Dinda in cooking; ask her to measure 1/2 + 1/4 cups",
                    "frequency": "2-3x per week",
                    "estimated_minutes": 15,
                }
            ],
            "message_to_parent": "Hi Ibu Sari! Dinda is a bright and creative learner. "
                                  "We're focusing on fractions right now, and I'd love your "
                                  "help at home. Try involving her in cooking or baking where "
                                  "she can see fractions in real life. We'll have this sorted out soon!",
            "upcoming_actions": ["Parent-teacher check-in on Friday", "Progress quiz in 2 weeks"],
            "support_resources": [
                {
                    "title": "Khan Academy Fractions",
                    "type": "website",
                    "description": "Free interactive fraction lessons in Bahasa Indonesia",
                }
            ],
            "tone": "encouraging",
        },
        scheduling_result={
            "mcp_tool_calls": [
                {
                    "tool": "google_calendar",
                    "action": "create_event",
                    "parameters": {
                        "title": "Fraction Remediation Session — Dinda",
                        "start": "2026-04-15T14:00:00",
                        "duration_minutes": 30,
                    },
                    "simulated_response": {"status": "success", "id": "cal_evt_001"},
                }
            ],
            "calendar_events": [
                {
                    "title": "Fraction Remediation Session — Dinda",
                    "type": "intervention_session",
                    "date": "2026-04-15",
                    "time": "14:00",
                    "duration_minutes": 30,
                    "attendees": ["Dinda Permata", "Ms. Anita Rahmawati"],
                    "description": "CPA-based fraction remediation session",
                }
            ],
            "tasks_created": [
                {
                    "title": "Prepare fraction bar materials for Dinda",
                    "assignee": "teacher",
                    "due_date": "2026-04-14",
                    "description": "Print and laminate fraction strip cards",
                    "priority": "high",
                }
            ],
            "reminders_set": [
                {
                    "title": "Check-in: Dinda's fraction progress",
                    "recipient": "Ibu Sari Dewi",
                    "send_at": "2026-04-17T08:00:00",
                    "channel": "email",
                    "message": "Friendly reminder to practice fractions with Dinda this weekend!",
                }
            ],
            "scheduling_summary": "3 intervention sessions scheduled for weeks 1-2. Parent reminder set.",
        },
        unified_response={
            "summary": "Orchestration complete. Dinda's fraction struggles have been analyzed. "
                       "A 2-week visual remediation plan is now active. Parent has been informed "
                       "with home practice suggestions. Three intervention sessions scheduled.",
            "actions_taken": 4,
            "next_checkpoint": "2026-04-28",
        },
        status="success",
        execution_time_ms=3420,
    )
    db.add(log)
    await db.commit()
    logger.info("Seed data inserted successfully.")
