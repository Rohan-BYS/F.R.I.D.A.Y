---
name: pc_hardware_diagnostic_triage
description: Decodes Motherboard POST beep codes, thermal throttling delta temperatures, and power supply rail tolerances.
category: blue_collar
version: 1.0.0
created_at: 2026-09-25 01:38:06
---

# 🧠 Learned Skill: pc_hardware_diagnostic_triage

> Decodes Motherboard POST beep codes, thermal throttling delta temperatures, and power supply rail tolerances.

## Implementation Code
```python
def diagnose_pc_hardware(beep_pattern: str, cpu_temp_c: float, psu_12v_actual: float) -> dict:
    beep_code_table = {
        "1_LONG_2_SHORT": "GPU / Display adapter initialization failure",
        "CONTINUOUS_SHORT": "RAM failure or power supply issue",
        "1_LONG_3_SHORT": "Memory detection error",
        "5_SHORT": "CPU failure or socket seating error"
    }
    diagnosis = beep_code_table.get(beep_pattern.upper(), "Standard boot or unknown beep pattern")
    is_throttling = cpu_temp_c >= 95.0
    psu_deviation_pct = abs(psu_12v_actual - 12.0) / 12.0 * 100.0
    psu_unstable = psu_deviation_pct > 5.0 # ATX spec allows +-5%
    return {
        "beep_code_diagnosis": diagnosis,
        "cpu_thermal_critical": is_throttling,
        "psu_12v_voltage_deviation_pct": round(psu_deviation_pct, 2),
        "psu_out_of_spec": psu_unstable,
        "action_required": "Replace thermal paste" if is_throttling else ("Check 12V PSU rail" if psu_unstable else "Hardware operating within normal specs")
    }
```

## Validation Tests
```python
res = diagnose_pc_hardware("1_LONG_2_SHORT", 98.0, 11.2)
assert "GPU" in res["beep_code_diagnosis"]
assert res["cpu_thermal_critical"] is True
assert res["psu_out_of_spec"] is True
```
