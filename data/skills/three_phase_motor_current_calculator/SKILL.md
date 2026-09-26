---
name: three_phase_motor_current_calculator
description: Calculates 3-phase electric motor full-load amperes (FLA) and NEC-compliant dual-element fuse sizing.
category: blue_collar
version: 1.0.0
created_at: 2026-09-25 01:38:08
---

# 🧠 Learned Skill: three_phase_motor_current_calculator

> Calculates 3-phase electric motor full-load amperes (FLA) and NEC-compliant dual-element fuse sizing.

## Implementation Code
```python
def calculate_motor_specs(horsepower: float, voltage: float = 460.0, efficiency_pct: float = 90.0, power_factor: float = 0.85) -> dict:
    import math
    watts = horsepower * 746.0
    eff = efficiency_pct / 100.0
    # I = P / (sqrt(3) * V * PF * Eff)
    fla = watts / (math.sqrt(3.0) * voltage * power_factor * eff)
    # NEC 430.52 Dual Element Fuse: 175% of FLA
    fuse_rating = fla * 1.75
    # Inverse Time Circuit Breaker: 250% of FLA
    breaker_rating = fla * 2.50
    return {
        "horsepower": horsepower,
        "full_load_amperes": round(fla, 2),
        "nec_dual_element_fuse_amps": round(fuse_rating, 1),
        "nec_circuit_breaker_amps": round(breaker_rating, 1)
    }
```

## Validation Tests
```python
res = calculate_motor_specs(25.0, 460.0)
assert res["full_load_amperes"] > 25.0
assert res["nec_circuit_breaker_amps"] > res["full_load_amperes"]
```
