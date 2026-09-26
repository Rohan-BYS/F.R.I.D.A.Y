---
name: concall_transcript_analyst
display_name: Earnings ConCall Transcript Deep Analyst
category: Fundamental Analysis
version: 1.0.0
description: Parses 40-page quarterly earnings conference call transcripts into EBITDA guidance, Capex plans, and management tone changes.
---

# Earnings ConCall Transcript Deep Analyst

## Overview
Parses 40-page quarterly earnings conference call transcripts into EBITDA guidance, Capex plans, and management tone changes.

## Category
**Fundamental Analysis**

## Architecture & Logic
```python
def parse_concall_transcript(transcript_text):
    # Identifies management tone shifts (defensive vs bullish).
    # Highlights recurring analyst questions and unanswered concerns in the Q&A section.
    pass
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
