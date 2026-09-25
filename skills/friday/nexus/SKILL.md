---
name: friday_nexus
description: F.R.I.D.A.Y.'s Webhook Nexus and Background Scheduler. Securely handles inbound internet signals and recurring background tasks.
category: automation
---

# F.R.I.D.A.Y. Nexus & Scheduler

## Overview
The Nexus serves as F.R.I.D.A.Y.'s autonomous event listener and scheduler.
It allows the agent to:
1. Receive webhooks from external services (GitHub, WhatsApp events, custom sensors) via a local FastAPI interface.
2. Run periodic background jobs (e.g. daily diagnostics, automated reporting).

## Architecture & Security
- **API Server:** Built on FastAPI, bound exclusively to `127.0.0.1:8080` to prevent unauthorized external access.
- **Authentication:** All inbound webhooks require a Bearer token (`X-Friday-Token` header) for verification.
- **Execution:** Webhooks do not execute raw commands; they map payloads to predefined agent tasks which pass through standard permission layers.
- **Scheduler:** Powered by `APScheduler` for robust cron-style background jobs.

## Commands (Capabilities)
- `nexus_start()`: Starts the background FastAPI webhook listener and the task scheduler on `localhost:8080`.
- `nexus_status()`: Reports the current status of the Nexus and active scheduled jobs.
- `nexus_schedule_job(task_name, cron_expression)`: Schedules a recognized background task on a recurring interval.

## Usage
F.R.I.D.A.Y. should start the Nexus automatically via `nexus_start()` if background event listening is requested, or if setting up automated routines.
