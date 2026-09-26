#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Docker Service & DevOps Orchestrator
=================================================
Automates self-hosting of local micro-services (SearXNG private search,
n8n automation, Redis caching, Ollama inference containers) via Docker Compose.

Usage:
  python scripts/docker_service_orchestrator.py --service searxng --generate
  python scripts/docker_service_orchestrator.py --list-available
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DOCKER_SERVICES_DIR = PROJECT_ROOT / "data" / "docker_services"
DOCKER_SERVICES_DIR.mkdir(parents=True, exist_ok=True)

PRESET_SERVICES = {
    "searxng": {
        "name": "SearXNG Private Meta-Search Engine",
        "port": 8080,
        "description": "Zero-tracking, privacy-respecting private search aggregator across Google/Bing/DuckDuckGo.",
        "compose": """version: '3.7'
services:
  searxng:
    image: searxng/searxng:latest
    container_name: friday_searxng
    ports:
      - "8080:8080"
    environment:
      - BIND_ADDRESS=0.0.0.0:8080
    restart: unless-stopped
"""
    },
    "n8n": {
        "name": "n8n Workflow Automation",
        "port": 5678,
        "description": "Visual multi-service automation engine for webhook processing and social distribution.",
        "compose": """version: '3.7'
services:
  n8n:
    image: n8nio/n8n:latest
    container_name: friday_n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=127.0.0.1
    restart: unless-stopped
"""
    },
    "redis": {
        "name": "Redis In-Memory Key-Value Cache",
        "port": 6379,
        "description": "High-throughput ephemeral caching for high-frequency market streaming.",
        "compose": """version: '3.7'
services:
  redis:
    image: redis:alpine
    container_name: friday_redis
    ports:
      - "6379:6379"
    restart: unless-stopped
"""
    },
}


class DockerServiceOrchestrator:
    """Manages local microservice compose stacks."""

    def __init__(self, services_dir: Optional[Path] = None):
        self.services_dir = services_dir or DOCKER_SERVICES_DIR

    def generate_service(self, service_key: str) -> Dict[str, Any]:
        """Generates docker-compose.yml for a target microservice."""
        if service_key not in PRESET_SERVICES:
            return {"status": "ERROR", "message": f"Service '{service_key}' not in presets. Available: {list(PRESET_SERVICES.keys())}"}

        preset = PRESET_SERVICES[service_key]
        target_dir = self.services_dir / service_key
        target_dir.mkdir(parents=True, exist_ok=True)
        compose_file = target_dir / "docker-compose.yml"

        with open(compose_file, "w", encoding="utf-8") as f:
            f.write(preset["compose"])

        return {
            "status": "COMPOSE_GENERATED",
            "service": preset["name"],
            "port": preset["port"],
            "compose_file": str(compose_file.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "start_command": f"cd {target_dir} && docker compose up -d",
        }

    def list_services(self) -> List[Dict[str, Any]]:
        return [
            {"key": k, "name": v["name"], "port": v["port"], "description": v["description"]}
            for k, v in PRESET_SERVICES.items()
        ]


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Docker Service Orchestrator")
    parser.add_argument("--service", type=str, help="Service key (e.g. searxng, n8n, redis)")
    parser.add_argument("--list", action="store_true", help="List available preset services")
    args = parser.parse_args()

    orchestrator = DockerServiceOrchestrator()

    if args.service:
        res = orchestrator.generate_service(args.service.lower())
        print(json.dumps(res, indent=2))
    else:
        services = orchestrator.list_services()
        print(json.dumps(services, indent=2))


if __name__ == "__main__":
    main()
