---
name: supply_chain_inventory_eoq_calculator
description: Calculates Economic Order Quantity (EOQ), reorder safety stock buffer, and annual holding cost trade-offs.
category: blue_collar
version: 1.0.0
created_at: 2026-09-25 01:38:07
---

# 🧠 Learned Skill: supply_chain_inventory_eoq_calculator

> Calculates Economic Order Quantity (EOQ), reorder safety stock buffer, and annual holding cost trade-offs.

## Implementation Code
```python
def calculate_inventory_eoq(annual_demand_units: float, cost_per_order: float, annual_holding_cost_per_unit: float, lead_time_days: float, daily_usage_variance_std: float) -> dict:
    # EOQ = sqrt( (2 * D * S) / H )
    eoq = ((2.0 * annual_demand_units * cost_per_order) / annual_holding_cost_per_unit) ** 0.5 if annual_holding_cost_per_unit > 0 else 0.0
    daily_demand = annual_demand_units / 365.0
    lead_time_demand = daily_demand * lead_time_days
    # Safety stock for 95% service level (Z = 1.65)
    safety_stock = 1.65 * (lead_time_days ** 0.5) * daily_usage_variance_std
    reorder_point = lead_time_demand + safety_stock
    return {
        "economic_order_quantity_units": round(eoq, 1),
        "lead_time_demand_units": round(lead_time_demand, 1),
        "recommended_safety_stock_units": round(safety_stock, 1),
        "reorder_point_units": round(reorder_point, 1)
    }
```

## Validation Tests
```python
res = calculate_inventory_eoq(10000.0, 50.0, 2.0, 10.0, 5.0)
assert res["economic_order_quantity_units"] > 500.0
assert res["reorder_point_units"] > res["lead_time_demand_units"]
```
