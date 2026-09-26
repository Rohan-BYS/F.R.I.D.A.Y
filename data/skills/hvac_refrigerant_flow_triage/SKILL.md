---
name: hvac_refrigerant_flow_triage
description: Calculates HVAC superheat and subcooling metrics to detect refrigerant leaks, overcharges, or airflow restrictions.
category: blue_collar
version: 1.0.0
created_at: 2026-09-25 01:38:06
---

# 🧠 Learned Skill: hvac_refrigerant_flow_triage

> Calculates HVAC superheat and subcooling metrics to detect refrigerant leaks, overcharges, or airflow restrictions.

## Implementation Code
```python
def triage_hvac_system(target_superheat_f: float, actual_superheat_f: float, target_subcooling_f: float, actual_subcooling_f: float) -> dict:
    sh_delta = actual_superheat_f - target_superheat_f
    sc_delta = actual_subcooling_f - target_subcooling_f
    if sh_delta > 5.0 and sc_delta < -5.0:
        diagnosis = "UNDERCHARGED (Refrigerant Leak)"
    elif sh_delta < -5.0 and sc_delta > 5.0:
        diagnosis = "OVERCHARGED (Excess Refrigerant)"
    elif sh_delta < -5.0 and sc_delta < -5.0:
        diagnosis = "LOW_AIRFLOW (Dirty filter or failing blower fan)"
    else:
        diagnosis = "NORMAL_CHARGE_AND_AIRFLOW"
    return {
        "superheat_variance_f": round(sh_delta, 1),
        "subcooling_variance_f": round(sc_delta, 1),
        "primary_diagnostic": diagnosis,
        "requires_technician_action": diagnosis != "NORMAL_CHARGE_AND_AIRFLOW"
    }
```

## Validation Tests
```python
res = triage_hvac_system(12.0, 20.0, 10.0, 3.0)
assert res["primary_diagnostic"] == "UNDERCHARGED (Refrigerant Leak)"
assert res["requires_technician_action"] is True
```
