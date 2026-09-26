---
name: ui_ux_fitts_law_click_target_calculator
description: Calculates movement index of difficulty using Fitts's Law and verifies accessibility minimum target dimensions.
category: design
version: 1.0.0
created_at: 2026-09-25 01:38:08
---

# 🧠 Learned Skill: ui_ux_fitts_law_click_target_calculator

> Calculates movement index of difficulty using Fitts's Law and verifies accessibility minimum target dimensions.

## Implementation Code
```python
def calculate_fitts_difficulty(target_width_px: float, distance_px: float) -> dict:
    import math
    if target_width_px <= 0 or distance_px <= 0:
        return {"error": "Invalid dimensions"}
    # Fitts's Law Index of Difficulty: ID = log2( (2 * D) / W )
    index_of_difficulty = math.log2((2.0 * distance_px) / target_width_px)
    meets_wcag_touch_target = target_width_px >= 44.0 # 44x44px minimum for mobile touch
    return {
        "target_width_px": target_width_px,
        "distance_px": distance_px,
        "index_of_difficulty_bits": round(index_of_difficulty, 2),
        "meets_mobile_touch_standard_44px": meets_wcag_touch_target,
        "ergonomic_rating": "EFFORTLESS" if index_of_difficulty < 3.0 else ("ACCEPTABLE" if index_of_difficulty < 5.0 else "HIGH_FRICTION")
    }
```

## Validation Tests
```python
res = calculate_fitts_difficulty(48.0, 150.0)
assert res["meets_mobile_touch_standard_44px"] is True
assert res["ergonomic_rating"] in ["EFFORTLESS", "ACCEPTABLE"]
```
