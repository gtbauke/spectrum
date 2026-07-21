import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

import aio_pika
from fastapi import APIRouter, Depends, Header, HTTPException, Response
from fastapi.responses import HTMLResponse

from core.common.config import Settings
from db.common.session import AsyncSessionLocal
from db.features.workers.repository import WorkerHeartbeatRepository

from app.state import state

logger = logging.getLogger(__name__)

admin_router = APIRouter()

_settings = Settings()

ADMIN_STATIC_DIR = Path(__file__).parent / "static"
CONTROL_EXCHANGE = "spectrum.control"


def _require_admin_key(
    authorization: Annotated[str | None, Header()] = None,
) -> None:
    """Dependency that validates the admin API key."""
    if not _settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Admin API key not configured on server",
        )

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Accept "Bearer <key>" or bare "<key>"
    token = authorization.removeprefix("Bearer ").strip()

    if token != _settings.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin API key")


# ---------------------------------------------------------------------------
# HTML dashboard
# ---------------------------------------------------------------------------

@admin_router.get("/workers", response_class=HTMLResponse)
async def admin_dashboard():
    """Serve the standalone admin dashboard page."""
    html_path = ADMIN_STATIC_DIR / "admin_page.html"

    if not html_path.exists():
        raise HTTPException(status_code=500, detail="Admin page not found")

    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# JSON API
# ---------------------------------------------------------------------------

@admin_router.get("/api/workers")
async def list_workers(_: None = Depends(_require_admin_key)):
    """Return a JSON list of all worker heartbeats with computed health."""
    async with AsyncSessionLocal() as session:
        repo = WorkerHeartbeatRepository(session)
        heartbeats = await repo.list_all()

    now = datetime.now(tz=timezone.utc)

    workers = []
    for hb in heartbeats:
        heartbeat_age_s = (now - hb.last_heartbeat).total_seconds()

        # Determine health
        if heartbeat_age_s > _settings.WORKER_STALENESS_SECONDS:
            health = "stale"
        elif (
            hb.status == "busy"
            and hb.task_started_at
            and (now - hb.task_started_at).total_seconds()
            > _settings.WORKER_TASK_TIMEOUT_SECONDS
        ):
            health = "task_timeout"
        else:
            health = "healthy"

        task_duration_s = None
        if hb.task_started_at and hb.status == "busy":
            task_duration_s = round((now - hb.task_started_at).total_seconds(), 1)

        workers.append(
            {
                "worker_id": hb.worker_id,
                "worker_type": hb.worker_type,
                "status": hb.status,
                "health": health,
                "current_task": hb.current_task,
                "task_duration_seconds": task_duration_s,
                "last_heartbeat_age_seconds": round(heartbeat_age_s, 1),
                "last_heartbeat": hb.last_heartbeat.isoformat(),
                "started_at": hb.started_at.isoformat(),
            }
        )

    return {"workers": workers}


@admin_router.post("/api/workers/{worker_id}/restart")
async def restart_worker(
    worker_id: str,
    _: None = Depends(_require_admin_key),
):
    """Send a restart command to a specific worker via RabbitMQ."""
    if not state.rabbitmq_connection:
        raise HTTPException(
            status_code=503, detail="RabbitMQ connection not available"
        )

    try:
        channel = await state.rabbitmq_connection.channel()
        exchange = await channel.declare_exchange(
            name=CONTROL_EXCHANGE,
            type=aio_pika.ExchangeType.DIRECT,
            durable=True,
        )

        message = aio_pika.Message(
            body=json.dumps({"command": "restart"}).encode("utf-8"),
            content_type="application/json",
        )

        routing_key = f"control.{worker_id}"
        await exchange.publish(message, routing_key=routing_key)
        await channel.close()

        logger.info("Restart command sent to worker '%s'", worker_id)
        return {"status": "ok", "message": f"Restart command sent to {worker_id}"}

    except Exception:
        logger.exception("Failed to send restart command to '%s'", worker_id)
        raise HTTPException(
            status_code=500, detail="Failed to send restart command"
        )
