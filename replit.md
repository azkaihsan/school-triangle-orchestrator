# School Triangle Orchestrator

## Overview

Multi-agent AI system connecting students, teachers, and parents in education. Built for Pastilulus — Google Cloud Gen AI Academy APAC Edition. This is a pure API-based system (no frontend) powered by Python + FastAPI and Gemini AI.

## Architecture

The **Primary Orchestrator Agent** receives an external trigger (e.g., "student is struggling in fractions") and coordinates four specialized sub-agents in sequence:

1. **Student Insight Agent** — Analyzes misconceptions and mastery gaps using Gemini AI
2. **Teacher Action Agent** — Generates targeted intervention plans and assignments
3. **Parent Communication Agent** — Prepares holistic progress summaries and home suggestions
4. **Scheduling Agent** — Simulates MCP tool calls to create calendar events, tasks, and reminders

All agents return structured JSON responses and results are persisted to the database. The orchestrator returns a single unified API response.

## Stack

- **Monorepo tool**: pnpm workspaces (workspace root is TypeScript; API server is Python)
- **API framework**: Python + FastAPI (async) with Uvicorn
- **Database**: PostgreSQL (AlloyDB-compatible mock) via SQLAlchemy async + asyncpg
- **AI**: Gemini 2.5 Flash via Replit AI Integrations (no user API key required)
- **OpenAPI docs**: Available at `/api/docs` (FastAPI auto-generated)

## Key Commands

- `bash artifacts/api-server/start.sh` — run API server locally (auto-reloads)
- FastAPI docs: `http://localhost:8080/api/docs`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/healthz` | Health check |
| GET | `/api/students` | List all students |
| POST | `/api/students` | Create a student |
| GET | `/api/students/{id}` | Get student with teacher/parent |
| PATCH | `/api/students/{id}` | Update student |
| DELETE | `/api/students/{id}` | Delete student |
| GET | `/api/students/{id}/insights` | Student Insight Agent (AI) |
| GET | `/api/students/{id}/interventions` | Teacher Action Agent (AI) |
| GET | `/api/students/{id}/parent-summary` | Parent Communication Agent (AI) |
| POST | `/api/orchestrate` | **Primary Orchestrator** — runs all 4 agents |
| GET | `/api/orchestrate/logs` | Orchestration audit logs |
| POST | `/api/schedule` | Scheduling Agent with simulated MCP tool calls |
| GET | `/api/docs` | FastAPI interactive Swagger UI |

## Database Schema

Tables managed by SQLAlchemy (auto-created on startup):
- `teachers` — teacher profiles
- `parents` — parent profiles  
- `students` — student profiles with teacher/parent FKs
- `curriculum_topics` — subject topics with learning objectives
- `interventions` — AI-generated intervention plans per student
- `assignments` — AI-generated student assignments
- `parent_notifications` — parent communication records
- `orchestration_logs` — full audit log of orchestration runs (per-agent JSON results)

## Seed Data

On first run, realistic seed data is auto-inserted:
- 2 teachers (Math, Science)
- 3 parents
- 3 students (Dinda Permata, Rizky Pratama, Aulia Safitri)
- 4 curriculum topics (Fractions, Scientific Notation, etc.)
- Sample interventions and orchestration logs

## Project Structure

```
artifacts/api-server/
├── app/
│   ├── main.py           # FastAPI app entry, lifespan (DB init + seed)
│   ├── database.py       # SQLAlchemy async engine (AlloyDB mock)
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── seed.py           # Realistic seed data
│   ├── agents/
│   │   ├── client.py     # Gemini AI client setup
│   │   ├── student_insight.py
│   │   ├── teacher_action.py
│   │   ├── parent_communication.py
│   │   └── scheduling.py
│   └── routes/
│       ├── health.py
│       ├── students.py
│       ├── orchestrate.py
│       └── schedule.py
├── requirements.txt
└── start.sh              # Server startup script
```
