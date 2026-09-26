---
name: elliott_wave_impulse_validator
description: Validates Elliott Wave impulse rules: Wave 2 cannot retrace >100% of Wave 1, Wave 3 cannot be shortest, Wave 4 cannot overlap Wave 1.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:45
---

# 🧠 Learned Skill: elliott_wave_impulse_validator

> Validates Elliott Wave impulse rules: Wave 2 cannot retrace >100% of Wave 1, Wave 3 cannot be shortest, Wave 4 cannot overlap Wave 1.

## Implementation Code
```python
def validate_elliott_impulse(w1_start: float, w1_end: float, w2_end: float, w3_end: float, w4_end: float, w5_end: float) -> dict:
    w1_len = abs(w1_end - w1_start)
    w2_retrace = abs(w2_end - w1_end)
    w3_len = abs(w3_end - w2_end)
    w4_retrace = abs(w4_end - w3_end)
    w5_len = abs(w5_end - w4_end)
    rules_violated = []
    # Rule 1: Wave 2 never moves beyond the start of Wave 1
    if w2_end <= w1_start:
        rules_violated.append("RULE_1_VIOLATED: Wave 2 retraced 100%+ of Wave 1.")
    # Rule 2: Wave 3 is never the shortest impulse wave
    if w3_len < w1_len and w3_len < w5_len:
        rules_violated.append("RULE_2_VIOLATED: Wave 3 is the shortest among waves 1, 3, and 5.")
    # Rule 3: Wave 4 never enters the price territory of Wave 1
    if w4_end <= w1_end:
        rules_violated.append("RULE_3_VIOLATED: Wave 4 overlaps with Wave 1 price territory.")
    is_valid = len(rules_violated) == 0
    return {
        "is_valid_elliott_impulse": is_valid,
        "wave_3_dominant": w3_len > w1_len and w3_len > w5_len,
        "violations": rules_violated,
        "guidance": "VALID_5_WAVE_IMPULSE: Prepare for ABC corrective cycle" if is_valid else "INVALID_COUNT: Recalibrate wave degrees or interpret as complex diagonal."
    }
```

## Validation Tests
```python
res = validate_elliott_impulse(100.0, 130.0, 115.0, 180.0, 140.0, 200.0)
assert res["is_valid_elliott_impulse"] is True
assert res["wave_3_dominant"] is True
```
