---
name: hardware_thermal_sentinel
display_name: Hardware & Thermal Overheat Sentinel
category: Host Security & Maintenance
version: 1.0.0
description: Continuously checks CPU/GPU temperatures, disk storage, and RAM usage on physical host machine, auto-throttling on thermal spikes >85°C.
---

# Hardware & Thermal Overheat Sentinel

## Category
**Host Security & Maintenance**

## Overview
Continuously checks CPU/GPU temperatures, disk storage, and RAM usage on physical host machine, auto-throttling on thermal spikes >85°C.

## Operational Directives
1. Execute autonomously via sub-agent triggers or scheduled routines.
2. All financial actions must strictly follow risk parameters and record executions to SQLite database.
3. Thermal alarms (>85°C) must take precedence over heavy computational tasks to preserve physical machine longevity.
