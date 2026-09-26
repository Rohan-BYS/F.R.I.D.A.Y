---
name: electrical_circuit_safety_checker
description: Calculates wire gauge (AWG) ampacity limits, 80% circuit breaker loading, and voltage drop over distance.
category: blue_collar
version: 1.0.0
created_at: 2026-09-25 01:38:06
---

# 🧠 Learned Skill: electrical_circuit_safety_checker

> Calculates wire gauge (AWG) ampacity limits, 80% circuit breaker loading, and voltage drop over distance.

## Implementation Code
```python
def check_electrical_circuit(breaker_amps: float, continuous_load_amps: float, wire_gauge_awg: int, distance_feet: float, voltage: float = 120.0) -> dict:
    max_continuous_safe_load = breaker_amps * 0.80 # 80% NEC Rule
    awg_max_ampacity = {14: 15, 12: 20, 10: 30, 8: 40, 6: 55}
    wire_limit = awg_max_ampacity.get(wire_gauge_awg, 15)
    wire_adequate = wire_limit >= breaker_amps
    overloaded = continuous_load_amps > max_continuous_safe_load
    # Voltage drop estimate: 2 * L * R * I / 1000
    resistance_per_1000ft = {14: 3.07, 12: 1.93, 10: 1.21, 8: 0.764, 6: 0.491}
    r = resistance_per_1000ft.get(wire_gauge_awg, 2.0)
    voltage_drop = (2.0 * distance_feet * r * continuous_load_amps) / 1000.0
    voltage_drop_pct = (voltage_drop / voltage) * 100.0
    return {
        "breaker_rating_amps": breaker_amps,
        "max_continuous_load_amps": round(max_continuous_safe_load, 1),
        "is_safe_under_80pct_rule": not overloaded,
        "wire_gauge_adequate_for_breaker": wire_adequate,
        "estimated_voltage_drop_pct": round(voltage_drop_pct, 2),
        "voltage_drop_acceptable": voltage_drop_pct <= 3.0
    }
```

## Validation Tests
```python
res = check_electrical_circuit(20.0, 15.0, 12, 50.0, 120.0)
assert res["is_safe_under_80pct_rule"] is True
assert res["wire_gauge_adequate_for_breaker"] is True
assert res["voltage_drop_acceptable"] is True
```
