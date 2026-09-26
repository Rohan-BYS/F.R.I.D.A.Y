---
name: viral_copywriting_engine
description: Formats copy into AIDA (Attention, Interest, Desire, Action) and PAS (Problem, Agitate, Solve) frameworks.
category: content
version: 1.0.0
created_at: 2026-09-25 01:38:05
---

# 🧠 Learned Skill: viral_copywriting_engine

> Formats copy into AIDA (Attention, Interest, Desire, Action) and PAS (Problem, Agitate, Solve) frameworks.

## Implementation Code
```python
def format_copywriting_framework(framework: str, hook: str, core_content: str, cta: str) -> dict:
    fw = framework.upper()
    if fw == "PAS":
        formatted = f"🔴 PROBLEM: {hook}\n⚡ AGITATION: Most people ignore this until it costs them thousands.\n💡 SOLUTION: {core_content}\n👉 ACTION: {cta}"
    elif fw == "BAB":
        formatted = f"BEFORE: {hook}\nAFTER: Imagine doing this in half the time without stress.\nBRIDGE: Here is the blueprint: {core_content}\nNEXT STEP: {cta}"
    else:  # Default AIDA
        formatted = f"🚨 ATTENTION: {hook}\n🔍 INTEREST: Did you know 90% of operators make this fatal mistake?\n✨ DESIRE: {core_content}\n🎯 ACTION: {cta}"
    word_count = len(formatted.split())
    return {
        "framework": fw,
        "formatted_copy": formatted,
        "word_count": word_count,
        "estimated_reading_seconds": round((word_count / 200.0) * 60, 1)
    }
```

## Validation Tests
```python
res = format_copywriting_framework("PAS", "Your memory leaks are crashing production.", "Use WAL SQLite.", "Clone FRIDAY today.")
assert "🔴 PROBLEM" in res["formatted_copy"]
assert res["word_count"] > 10
```
