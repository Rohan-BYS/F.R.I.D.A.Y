---
name: video_script_retention_architect
description: Structures 60-second Short/Reel scripts with 3-second visual hooks, pattern interrupts, and payoff loops.
category: content
version: 1.0.0
created_at: 2026-09-25 01:38:05
---

# 🧠 Learned Skill: video_script_retention_architect

> Structures 60-second Short/Reel scripts with 3-second visual hooks, pattern interrupts, and payoff loops.

## Implementation Code
```python
def structure_short_video_script(topic: str, core_insight: str, visual_hook: str) -> dict:
    return {
        "topic": topic,
        "timeline": [
            {"seconds": "00-03", "cue": "VISUAL_HOOK", "action": f"Camera zoom-in. Display bold text: '{visual_hook}'"},
            {"seconds": "03-15", "cue": "THE_COMMON_LIE", "action": "Debunk the status quo approach with visceral proof."},
            {"seconds": "15-35", "cue": "THE_BREAKTHROUGH", "action": f"Demonstrate step-by-step: {core_insight}"},
            {"seconds": "35-50", "cue": "PATTERN_INTERRUPT", "action": "Cut to screen recording or fast animation before viewer scrolls."},
            {"seconds": "50-60", "cue": "CALL_TO_ACTION", "action": "Loop seamless transition back to the first second."}
        ],
        "seamless_loop_tip": "Make your final sentence connect grammatically to your opening hook."
    }
```

## Validation Tests
```python
res = structure_short_video_script("Local AI", "Run DeepSeek on your laptop", "Stop paying API fees")
assert len(res["timeline"]) == 5
assert res["timeline"][0]["cue"] == "VISUAL_HOOK"
```
