import sys
import subprocess
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn
import asyncio
import os

app = FastAPI(
    title="F.R.I.D.A.Y. Omni-Agent API",
    description="REST API interface for F.R.I.D.A.Y. capabilities.",
    version="1.0.0"
)

# Fix Windows Unicode Encode Error for subprocess outputs
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

class CommandRequest(BaseModel):
    command: str
    args: list[str] = []

class AgentTask(BaseModel):
    prompt: str
    context: str = ""

@app.get("/")
def read_root():
    return {"status": "online", "system": "F.R.I.D.A.Y. Omni-Agent", "version": "1.0.0"}

@app.post("/execute/cli")
def execute_cli_command(req: CommandRequest):
    """Executes a friday CLI command (e.g., 'market', 'chart', 'health')"""
    try:
        full_command = ["python", "friday_cli.py", req.command] + req.args
        result = subprocess.run(full_command, capture_output=True, text=True, check=True, encoding="utf-8")
        return {"status": "success", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Command failed: {e.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute/task")
async def execute_agent_task(task: AgentTask, background_tasks: BackgroundTasks):
    """
    Submits a natural language task to F.R.I.D.A.Y.'s Orchestrator asynchronously.
    """
    def run_task_sync():
        try:
            # Here we would interface with friday_engine.core.engine
            # For now, we simulate a subprocess call to a hypothetical agent trigger
            subprocess.run(["python", "friday_cli.py", "curiosity"], capture_output=True, text=True)
        except Exception as e:
            print(f"Agent Task Error: {e}")

    background_tasks.add_task(run_task_sync)
    return {"status": "accepted", "message": "Task queued for autonomous execution.", "task": task.prompt}

if __name__ == "__main__":
    print("🚀 Starting F.R.I.D.A.Y. API Server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
