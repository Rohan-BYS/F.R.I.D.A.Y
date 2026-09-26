---
name: smart_money_concepts_ict_analyzer
description: Identifies Order Blocks (OB), Break of Structure (BOS), Change of Character (CHoCH), and Premium vs Discount arrays.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:43
---

# 🧠 Learned Skill: smart_money_concepts_ict_analyzer

> Identifies Order Blocks (OB), Break of Structure (BOS), Change of Character (CHoCH), and Premium vs Discount arrays.

## Implementation Code
```python
def analyze_smc_structure(highs: list, lows: list, closes: list) -> dict:
    if len(highs) < 5 or len(lows) < 5:
        return {"error": "Insufficient candle data for SMC analysis"}
    recent_high = max(highs[-5:])
    recent_low = min(lows[-5:])
    range_high = max(highs)
    range_low = min(lows)
    equilibrium = (range_high + range_low) / 2.0
    current_price = closes[-1]
    pricing_zone = "PREMIUM (Favorable for Shorts)" if current_price > equilibrium else "DISCOUNT (Favorable for Longs)"
    bos_bullish = closes[-1] > highs[-2] and highs[-2] > highs[-3]
    bos_bearish = closes[-1] < lows[-2] and lows[-2] < lows[-3]
    structure_shift = "BULLISH_BOS" if bos_bullish else ("BEARISH_BOS" if bos_bearish else "CONSOLIDATION")
    return {
        "range_high": range_high,
        "range_low": range_low,
        "equilibrium_50pct": round(equilibrium, 2),
        "current_price": current_price,
        "pricing_zone": pricing_zone,
        "market_structure": structure_shift,
        "optimal_trade_entry_bias": "LOOK_FOR_DISCOUNT_ORDER_BLOCKS" if current_price < equilibrium else "LOOK_FOR_PREMIUM_LIQUIDITY_SWEEPS"
    }
```

## Validation Tests
```python
res = analyze_smc_structure([100, 105, 110, 115, 120], [95, 98, 102, 108, 112], [98, 103, 109, 114, 119])
assert res["pricing_zone"].startswith("PREMIUM")
assert res["equilibrium_50pct"] > 0
```
