---
name: fibonacci_retracement_golden_pocket
description: Calculates Fibonacci retracement levels, Optimal Trade Entry (OTE: 0.618 - 0.786), and extension profit targets (1.272, 1.618).
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:43
---

# 🧠 Learned Skill: fibonacci_retracement_golden_pocket

> Calculates Fibonacci retracement levels, Optimal Trade Entry (OTE: 0.618 - 0.786), and extension profit targets (1.272, 1.618).

## Implementation Code
```python
def calculate_fibonacci_levels(swing_low: float, swing_high: float, trend: str = "bullish") -> dict:
    diff = swing_high - swing_low
    if trend.lower() == "bullish":
        fibs = {
            "0.236": round(swing_high - 0.236 * diff, 2),
            "0.382": round(swing_high - 0.382 * diff, 2),
            "0.500_equilibrium": round(swing_high - 0.500 * diff, 2),
            "0.618_golden_ratio": round(swing_high - 0.618 * diff, 2),
            "0.650_golden_pocket": round(swing_high - 0.650 * diff, 2),
            "0.786_deep_retrace": round(swing_high - 0.786 * diff, 2),
            "1.272_extension_target": round(swing_high + 0.272 * diff, 2),
            "1.618_golden_extension": round(swing_high + 0.618 * diff, 2)
        }
    else:
        fibs = {
            "0.236": round(swing_low + 0.236 * diff, 2),
            "0.382": round(swing_low + 0.382 * diff, 2),
            "0.500_equilibrium": round(swing_low + 0.500 * diff, 2),
            "0.618_golden_ratio": round(swing_low + 0.618 * diff, 2),
            "0.650_golden_pocket": round(swing_low + 0.650 * diff, 2),
            "0.786_deep_retrace": round(swing_low + 0.786 * diff, 2),
            "1.272_extension_target": round(swing_low - 0.272 * diff, 2),
            "1.618_golden_extension": round(swing_low - 0.618 * diff, 2)
        }
    return {
        "trend_direction": trend.upper(),
        "golden_pocket_range": f"{fibs['0.618_golden_ratio']} - {fibs['0.650_golden_pocket']}",
        "fibonacci_levels": fibs
    }
```

## Validation Tests
```python
res = calculate_fibonacci_levels(100.0, 200.0, "bullish")
assert res["fibonacci_levels"]["0.500_equilibrium"] == 150.0
assert res["fibonacci_levels"]["1.618_golden_extension"] == 261.8
```
