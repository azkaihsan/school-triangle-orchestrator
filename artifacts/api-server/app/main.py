import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text

from .database import engine, Base, AsyncSessionLocal
from .models import (  # noqa: F401 — imported to register with Base metadata
    Teacher, Parent, Student, CurriculumTopic,
    Intervention, Assignment, ParentNotification, OrchestrationLog,
)
from .routes.health import router as health_router
from .routes.students import router as students_router
from .routes.orchestrate import router as orchestrate_router
from .routes.schedule import router as schedule_router
from .seed import seed_if_empty

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting School Triangle Orchestrator API...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as db:
        await seed_if_empty(db)
    logger.info("Database ready.")
    yield
    logger.info("Shutting down...")
    await engine.dispose()


app = FastAPI(
    title="School Triangle Orchestrator API",
    description=(
        "Multi-agent AI system connecting students, teachers, and parents. "
        "Powered by Gemini AI. Built for Pastilulus — Google Cloud Gen AI Academy APAC Edition."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.include_router(health_router, prefix="/api")
app.include_router(students_router, prefix="/api")
app.include_router(orchestrate_router, prefix="/api")
app.include_router(schedule_router, prefix="/api")
