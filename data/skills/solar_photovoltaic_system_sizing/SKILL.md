---
name: solar_photovoltaic_system_sizing
description: Calculates solar panel array kW requirements, battery storage kWh, and payback years from utility rates.
category: blue_collar
version: 1.0.0
created_at: 2026-09-25 01:38:08
---

# 🧠 Learned Skill: solar_photovoltaic_system_sizing

> Calculates solar panel array kW requirements, battery storage kWh, and payback years from utility rates.

## Implementation Code
```python
def size_solar_pv_system(monthly_kwh_usage: float, peak_sun_hours_per_day: float = 4.5, utility_rate_per_kwh: float = 0.18, cost_per_watt: float = 2.80) -> dict:
    daily_kwh = monthly_kwh_usage / 30.0
    system_efficiency = 0.80
    required_system_kw = daily_kwh / (peak_sun_hours_per_day * system_efficiency)
    total_system_cost = required_system_kw * 1000.0 * cost_per_watt
    annual_electric_savings = monthly_kwh_usage * utility_rate_per_kwh * 12.0
    payback_years = (total_system_cost / annual_electric_savings) if annual_electric_savings > 0 else 99.0
    battery_storage_kwh = daily_kwh * 1.2 # 1.2 days of autonomy
    return {
        "recommended_array_size_kw": round(required_system_kw, 2),
        "recommended_battery_kwh": round(battery_storage_kwh, 2),
        "estimated_gross_cost": round(total_system_cost, 2),
        "annual_utility_savings": round(annual_electric_savings, 2),
        "simple_payback_years": round(payback_years, 1)
    }
```

## Validation Tests
```python
res = size_solar_pv_system(900.0)
assert res["recommended_array_size_kw"] > 5.0
assert res["simple_payback_years"] < 15.0
```
