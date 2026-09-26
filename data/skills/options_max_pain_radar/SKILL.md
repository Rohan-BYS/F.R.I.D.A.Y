---
name: options_max_pain_radar
display_name: Options Chain & Max Pain Radar
category: Derivatives & Options
version: 1.0.0
description: Calculates Put-Call Ratio (PCR), Call/Put Open Interest concentration walls, and solves for the Max Pain expiry pin price.
---

# Options Chain & Max Pain Radar

## Category
**Derivatives & Options**

## Overview
Calculates Put-Call Ratio (PCR), Call/Put Open Interest concentration walls, and solves for the Max Pain expiry pin price.

## Operational Directives
1. Execute autonomously via sub-agent triggers or scheduled routines.
2. All financial actions must strictly follow risk parameters and record executions to SQLite database.
3. Thermal alarms (>85°C) must take precedence over heavy computational tasks to preserve physical machine longevity.
