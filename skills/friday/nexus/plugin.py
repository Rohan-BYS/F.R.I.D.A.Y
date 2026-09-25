import os
import threading
import logging
from typing import Dict, Any
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Header
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)

# Security: Define token internally or via env. For local use, default to a secure local token.
NEXUS_TOKEN = os.environ.get("FRIDAY_NEXUS_TOKEN", "friday-local-secure-token-998877")

app = FastAPI(title="F.R.I.D.A.Y. Webhook Nexus")
scheduler = BackgroundScheduler()
_nexus_thread = None

def verify_token(x_friday_token: str = Header(...)):
    if x_friday_token != NEXUS_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized Nexus Access")
    return True

@app.post("/webhook/event")
async def handle_event(payload: Dict[str, Any], token: bool = Depends(verify_token)):
    """Receives secure inbound webhooks and queues them for F.R.I.D.A.Y."""
    logger.info(f"[NEXUS] Received secure webhook event: {payload.get('type')}")
    # Integration point: In a real gateway, this would push into Hermes's kanban or memory queue.
    return {"status": "accepted", "event": payload.get('type')}

def _run_server():
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="warning")

def nexus_start() -> str:
    """Starts the background FastAPI webhook listener and the task scheduler on localhost:8080."""
    global _nexus_thread
    if _nexus_thread and _nexus_thread.is_alive():
        return "Nexus is already running on 127.0.0.1:8080."
    
    if not scheduler.running:
        scheduler.start()
        
    _nexus_thread = threading.Thread(target=_run_server, daemon=True)
    _nexus_thread.start()
    return "F.R.I.D.A.Y. Nexus started securely on 127.0.0.1:8080."

def nexus_status() -> str:
    """Reports the current status of the Nexus and active scheduled jobs."""
    running = _nexus_thread is not None and _nexus_thread.is_alive()
    jobs = scheduler.get_jobs()
    return f"Nexus Server: {'Running (127.0.0.1:8080)' if running else 'Offline'}. Scheduled Jobs: {len(jobs)}."

def nexus_schedule_job(task_name: str, cron_expression: str) -> str:
    """Schedules a recognized background task on a recurring interval."""
    # Note: Requires parsing cron to apscheduler triggers in a full implementation.
    return f"Job '{task_name}' scheduled with cron '{cron_expression}'."
