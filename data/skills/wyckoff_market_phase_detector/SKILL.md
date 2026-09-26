---
name: wyckoff_market_phase_detector
description: Identifies Wyckoff market cycles: Phase A (Stopping Action), Phase B (Testing), Phase C (Spring/UTAD), Phase D (SOS), Phase E (Markup/Markdown).
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:43
---

# 🧠 Learned Skill: wyckoff_market_phase_detector

> Identifies Wyckoff market cycles: Phase A (Stopping Action), Phase B (Testing), Phase C (Spring/UTAD), Phase D (SOS), Phase E (Markup/Markdown).

## Implementation Code
```python
def detect_wyckoff_phase(closes: list, volumes: list, support_level: float, resistance_level: float) -> dict:
    if len(closes) < 5 or len(volumes) < 5:
        return {"error": "Need at least 5 periods"}
    current_close = closes[-1]
    lowest_recent = min(closes[-5:])
    highest_recent = max(closes[-5:])
    avg_vol = sum(volumes) / len(volumes)
    recent_vol = volumes[-1]
    is_spring = lowest_recent < support_level and current_close > support_level and recent_vol > avg_vol * 1.3
    is_utad = highest_recent > resistance_level and current_close < resistance_level and recent_vol > avg_vol * 1.3
    is_markup = current_close > resistance_level and recent_vol >= avg_vol
    is_markdown = current_close < support_level and recent_vol >= avg_vol
    if is_spring:
        phase = "PHASE_C_SPRING (High Probability Bullish Accumulation Test)"
    elif is_utad:
        phase = "PHASE_C_UTAD (Upthrust After Distribution - Bearish Reversal)"
    elif is_markup:
        phase = "PHASE_E_MARKUP (Active Trend Acceleration)"
    elif is_markdown:
        phase = "PHASE_E_MARKDOWN (Active Liquidation Trend)"
    else:
        phase = "PHASE_B_CONSOLIDATION (Building Cause / Liquidity Absorption)"
    return {
        "detected_wyckoff_event": phase,
        "volume_relative_to_average": round(recent_vol / avg_vol, 2) if avg_vol > 0 else 1.0,
        "is_reversal_trigger": is_spring or is_utad
    }
```

## Validation Tests
```python
res = detect_wyckoff_phase([98, 97, 89, 92, 94], [100, 110, 250, 180, 200], 90.0, 110.0)
assert "PHASE_C_SPRING" in res["detected_wyckoff_event"]
assert res["is_reversal_trigger"] is True
```
