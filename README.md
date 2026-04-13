# School Triangle Orchestrator

> **Multi-agent AI system connecting students, teachers, and parents.**  
> Built for **Pastilulus** — Google Cloud Gen AI Academy APAC Edition.

---

## Overview

The School Triangle Orchestrator is a pure API system (no frontend) that uses a **Primary Orchestrator Agent** to coordinate four specialized Gemini-powered sub-agents whenever a learning event is triggered (e.g. "student is struggling with fractions"). Each sub-agent handles a specific concern and the results are persisted to the database and returned as a single unified response.

```
Trigger (API call)
       │
       ▼
┌─────────────────────────────┐
│   Primary Orchestrator      │
└──────────────┬──────────────┘
               │ coordinates
   ┌───────────┼───────────────────┐
   ▼           ▼           ▼      ▼
Student    Teacher      Parent  Scheduling
Insight    Action       Comm.   Agent
Agent      Agent        Agent   (MCP sim)
```

---

## Sub-Agents

| Agent | Responsibility |
|---|---|
| **Student Insight Agent** | Analyzes misconceptions and mastery gaps |
| **Teacher Action Agent** | Generates targeted intervention plans and assignments |
| **Parent Communication Agent** | Prepares holistic progress summaries and home suggestions |
| **Scheduling Agent** | Simulates MCP tool calls — creates calendar events, tasks, and reminders |

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | Python + FastAPI (async) |
| Server | Uvicorn |
| Database | PostgreSQL — AlloyDB in production, local PostgreSQL in dev |
| ORM | SQLAlchemy (async) + asyncpg |
| AI | Gemini 2.5 Flash (`google-genai`) |
| Validation | Pydantic v2 |
| Container | Docker (Python 3.12-slim) |
| CI/CD | Google Cloud Build → Artifact Registry → Cloud Run |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/healthz` | Health check |
| GET | `/api/students` | List all students |
| POST | `/api/students` | Create a student |
| GET | `/api/students/{id}` | Get student with teacher & parent |
| PATCH | `/api/students/{id}` | Update student |
| DELETE | `/api/students/{id}` | Delete student |
| GET | `/api/students/{id}/insights` | Student Insight Agent (AI) |
| GET | `/api/students/{id}/interventions` | Teacher Action Agent (AI) |
| GET | `/api/students/{id}/parent-summary` | Parent Communication Agent (AI) |
| **POST** | **`/api/orchestrate`** | **Primary Orchestrator — runs all 4 agents** |
| GET | `/api/orchestrate/logs` | Orchestration audit logs |
| POST | `/api/schedule` | Scheduling Agent with MCP tool simulation |
| GET | `/api/docs` | Interactive Swagger UI |

### Orchestrate Request Example

```json
POST /api/orchestrate
{
  "student_id": 1,
  "trigger_description": "Student is struggling with fractions and failed last quiz",
  "topic": "Fractions"
}
```

### Orchestrate Response Structure

```json
{
  "orchestration_id": 42,
  "status": "success",
  "execution_time_ms": 3821,
  "agent_statuses": [
    { "agent": "student_insight",      "status": "success" },
    { "agent": "teacher_action",       "status": "success" },
    { "agent": "parent_communication", "status": "success" },
    { "agent": "scheduling",           "status": "success" }
  ],
  "student_insight":       { ... },
  "teacher_action":        { ... },
  "parent_communication":  { ... },
  "scheduling":            { ... },
  "summary": "Orchestration success for Dinda Permata (Grade 7). Mastery level: developing. ..."
}
```

---

## Project Structure

```
artifacts/api-server/
├── app/
│   ├── main.py                   # FastAPI app, lifespan (DB init + seed)
│   ├── database.py               # SQLAlchemy async engine (AlloyDB-compatible)
│   ├── models.py                 # ORM models
│   ├── schemas.py                # Pydantic request/response schemas
│   ├── seed.py                   # Realistic seed data (auto-runs on first start)
│   ├── agents/
│   │   ├── client.py             # Gemini client (supports GEMINI_API_KEY + Replit proxy)
│   │   ├── student_insight.py
│   │   ├── teacher_action.py
│   │   ├── parent_communication.py
│   │   └── scheduling.py
│   └── routes/
│       ├── health.py
│       ├── students.py
│       ├── orchestrate.py
│       └── schedule.py
├── Dockerfile                    # Production container (Python 3.12-slim)
├── cloudbuild.yaml               # Cloud Build CI/CD pipeline
├── requirements.txt
└── start.sh                      # Local dev startup script
```

---

## Database Schema

Tables are auto-created on startup via SQLAlchemy:

| Table | Description |
|---|---|
| `teachers` | Teacher profiles |
| `parents` | Parent profiles |
| `students` | Student profiles with teacher/parent FKs |
| `curriculum_topics` | Subject topics with learning objectives |
| `interventions` | AI-generated intervention plans |
| `assignments` | AI-generated student assignments |
| `parent_notifications` | Parent communication records |
| `orchestration_logs` | Full audit log of every orchestration run |

### Seed Data

On first run the app auto-inserts realistic Indonesian school data:
- 2 teachers (Math, Science)
- 3 parents
- 3 students: **Dinda Permata**, **Rizky Pratama**, **Aulia Safitri**
- 4 curriculum topics (Fractions, Scientific Notation, Photosynthesis, Algebra)
- Sample interventions and orchestration logs

---

## Running Locally

### Prerequisites
- Python 3.12+
- PostgreSQL running locally
- `GEMINI_API_KEY` **or** Replit AI Integration env vars

### Setup

```bash
cd artifacts/api-server
pip install -r requirements.txt

export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/school_triangle"
export GEMINI_API_KEY="your-key-from-aistudio.google.com"

bash start.sh
```

Open **http://localhost:8080/api/docs** for the interactive Swagger UI.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | Yes | PostgreSQL connection string (`postgresql+asyncpg://...`) |
| `GEMINI_API_KEY` | Yes* | Google AI Studio API key (for Cloud Run / local dev) |
| `AI_INTEGRATIONS_GEMINI_API_KEY` | Yes* | Replit AI Integration key (alternative to above) |
| `AI_INTEGRATIONS_GEMINI_BASE_URL` | Yes* | Replit AI Integration base URL |
| `PORT` | No | Server port (default: `8080`) |
| `NODE_ENV` | No | Set to `production` to disable hot-reload |

*Either `GEMINI_API_KEY` alone, or both `AI_INTEGRATIONS_*` vars are required.

---

## Deploy to Google Cloud Run

See **[DEPLOY.md](./DEPLOY.md)** for the full step-by-step guide including:
- Enabling GCP APIs
- Setting up Artifact Registry
- Storing secrets in Secret Manager
- Connecting to AlloyDB via VPC
- One-click deploy via Cloud Build

Quick deploy:
```bash
gcloud builds submit --config=cloudbuild.yaml \
  --substitutions=SHORT_SHA=$(git rev-parse --short HEAD) .
```

---

## License

MIT — Built for Google Cloud Gen AI Academy APAC Edition by **Pastilulus**.
