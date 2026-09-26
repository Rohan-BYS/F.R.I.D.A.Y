---
name: health_nutrition_macronutrient_calc
description: Calculates Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE), and protein/carb/fat grams.
category: daily_life
version: 1.0.0
created_at: 2026-09-25 01:38:03
---

# 🧠 Learned Skill: health_nutrition_macronutrient_calc

> Calculates Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE), and protein/carb/fat grams.

## Implementation Code
```python
def calculate_macros(weight_kg: float, height_cm: float, age: int, is_male: bool, activity_multiplier: float = 1.55, goal: str = "maintenance") -> dict:
    if is_male:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    tdee = bmr * activity_multiplier
    target_calories = tdee
    if goal == "cut":
        target_calories -= 500.0
    elif goal == "bulk":
        target_calories += 400.0
    protein_g = weight_kg * 2.0
    fat_g = (target_calories * 0.25) / 9.0
    carbs_g = (target_calories - (protein_g * 4.0 + fat_g * 9.0)) / 4.0
    return {
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "target_calories": round(target_calories, 1),
        "protein_grams": round(protein_g, 1),
        "fat_grams": round(fat_g, 1),
        "carbs_grams": round(carbs_g, 1)
    }
```

## Validation Tests
```python
macros = calculate_macros(75.0, 180.0, 28, True, 1.55, "cut")
assert macros["protein_grams"] == 150.0
assert macros["target_calories"] < macros["tdee"]
```
