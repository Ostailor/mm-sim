from __future__ import annotations

from celery import Celery
from loguru import logger

app = Celery("mm_sim", broker="redis://localhost:6379/0")


@app.task
def train(session_id: str) -> str:
    """Dummy training task."""
    logger.info(f"Training session {session_id}")
    return session_id

