"""
F.R.I.D.A.Y. Hive Mind - Worker Node Daemon.
Run this script on any computer on your network to give F.R.I.D.A.Y. remote control of its resources.
"""

import os
import sys
import subprocess
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Depends, Security
from pydantic import BaseModel
import httpx
import argparse
import socket
from fastapi.security import APIKeyHeader

app = FastAPI(title="F.R.I.D.A.Y. Worker Node")

API_KEY = os.environ.get("HIVE_MIND_API_KEY", "default-insecure-key-change-me")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

class ExecRequest(BaseModel):
    command: str
    timeout: int = 60

class FileWriteRequest(BaseModel):
    filepath: str
    content: str

@app.post("/execute")
async def execute_command(req: ExecRequest, api_key: str = Depends(verify_api_key)):
    """Executes a terminal command on this node and returns the output."""
    try:
        result = subprocess.run(
            req.command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=req.timeout
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Command execution timed out.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fs/read")
async def read_file(filepath: str, api_key: str = Depends(verify_api_key)):
    """Reads a file from this node."""
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found.")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return {"content": f.read()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/fs/write")
async def write_file(req: FileWriteRequest, api_key: str = Depends(verify_api_key)):
    """Writes a file to this node."""
    try:
        os.makedirs(os.path.dirname(req.filepath) or '.', exist_ok=True)
        with open(req.filepath, 'w', encoding='utf-8') as f:
            f.write(req.content)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def register_with_nexus(nexus_url: str, node_name: str, port: int):
    """Announce this node's existence to the main F.R.I.D.A.Y. brain."""
    try:
        res = httpx.post(f"{nexus_url}/hive/register", json={
            "node_name": node_name,
            "port": port,
            "capabilities": ["shell", "fs"]
        }, timeout=5.0)
        if res.status_code == 200:
            print(f"[SUCCESS] Successfully registered node '{node_name}' with Nexus at {nexus_url}")
        else:
            print(f"[WARN] Failed to register with Nexus: {res.text}")
    except Exception as e:
        print(f"[WARN] Could not connect to Nexus at {nexus_url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Hive Mind Worker Node")
    parser.add_argument("--name", type=str, default=socket.gethostname(), help="Name of this node (e.g. editor-pc)")
    parser.add_argument("--port", type=int, default=8081, help="Port to listen on")
    parser.add_argument("--nexus", type=str, default="http://localhost:8080", help="URL of the main F.R.I.D.A.Y. Nexus")
    args = parser.parse_args()

    print(f"Starting F.R.I.D.A.Y. Node '{args.name}' on port {args.port}...")
    register_with_nexus(args.nexus, args.name, args.port)
    
    uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="warning")
