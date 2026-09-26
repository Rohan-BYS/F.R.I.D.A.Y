---
name: executive_minto_pyramid_summarizer
description: Applies the Minto Pyramid Principle (Situation, Complication, Question, Answer) to executive decision briefs.
category: white_collar
version: 1.0.0
created_at: 2026-09-25 01:38:05
---

# 🧠 Learned Skill: executive_minto_pyramid_summarizer

> Applies the Minto Pyramid Principle (Situation, Complication, Question, Answer) to executive decision briefs.

## Implementation Code
```python
def structure_executive_brief(situation: str, complication: str, question: str, recommendation: str, key_arguments: list) -> dict:
    brief = (
        f"📌 EXECUTIVE SUMMARY (ANSWER FIRST):\n{recommendation}\n\n"
        f"CONTEXT:\n- Situation: {situation}\n- Complication: {complication}\n- Core Question: {question}\n\n"
        "STRATEGIC PILLARS:\n"
    )
    for idx, arg in enumerate(key_arguments, 1):
        brief += f"{idx}. {arg}\n"
    return {
        "governing_thought": recommendation,
        "scqa_formatted_brief": brief,
        "read_time_seconds": round(len(brief.split()) / 3.0)
    }
```

## Validation Tests
```python
brief = structure_executive_brief("Company revenue grew 20%", "Server costs tripled", "How to restore margin?", "Migrate to local offline inference.", ["Zero cloud API fees", "Higher data privacy"])
assert "📌 EXECUTIVE SUMMARY" in brief["scqa_formatted_brief"]
assert len(brief["governing_thought"]) > 5
```
