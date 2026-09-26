---
name: automotive_obd2_fault_analyzer
description: Interprets OBD-II Diagnostic Trouble Codes (DTC), fuel trim variances, and mass air flow symptoms.
category: blue_collar
version: 1.0.0
created_at: 2026-09-25 01:38:06
---

# 🧠 Learned Skill: automotive_obd2_fault_analyzer

> Interprets OBD-II Diagnostic Trouble Codes (DTC), fuel trim variances, and mass air flow symptoms.

## Implementation Code
```python
def analyze_obd2_code(dtc_code: str, long_term_fuel_trim_pct: float) -> dict:
    dtc_library = {
        "P0300": "Random/Multiple Cylinder Misfire Detected",
        "P0171": "System Too Lean (Bank 1) - possible vacuum leak or dirty MAF",
        "P0420": "Catalyst System Efficiency Below Threshold (Bank 1)",
        "P0128": "Coolant Thermostat (Coolant Temp Below Regulating Temp)"
    }
    code = dtc_code.upper().strip()
    description = dtc_library.get(code, "Generic powertrain trouble code")
    running_lean = long_term_fuel_trim_pct > 10.0
    running_rich = long_term_fuel_trim_pct < -10.0
    return {
        "dtc_code": code,
        "official_description": description,
        "fuel_trim_status": "LEAN" if running_lean else ("RICH" if running_rich else "STABLE"),
        "primary_suspect": "Intake vacuum leak or fuel injector clog" if running_lean else ("Oxygen sensor or ignition coil" if code == "P0300" else "Standard diagnostic inspection needed")
    }
```

## Validation Tests
```python
res = analyze_obd2_code("P0171", 14.5)
assert res["fuel_trim_status"] == "LEAN"
assert "MAF" in res["official_description"]
```
