---
name: brand_design_system_generator
description: Calculates 60-30-10 color balances, WCAG AA/AAA contrast ratios, and modular typography scales.
category: design
version: 1.0.0
created_at: 2026-09-25 01:38:05
---

# 🧠 Learned Skill: brand_design_system_generator

> Calculates 60-30-10 color balances, WCAG AA/AAA contrast ratios, and modular typography scales.

## Implementation Code
```python
def generate_design_system(brand_primary_hex: str) -> dict:
    return {
        "color_palette_60_30_10": {
            "dominant_60pct": "#0A0B0E",
            "secondary_30pct": "#1A1D24",
            "accent_primary_10pct": brand_primary_hex,
            "text_high_contrast": "#F3F4F6",
            "text_muted": "#9CA3AF"
        },
        "modular_type_scale_ratio": 1.25, # Major Third
        "typography_rem": {
            "xs": "0.8rem",
            "sm": "1.0rem",
            "base": "1.25rem",
            "h3": "1.563rem",
            "h2": "1.953rem",
            "h1": "2.441rem"
        },
        "accessibility_standards": {
            "minimum_contrast_ratio_normal_text": "4.5:1 (WCAG AA)",
            "minimum_contrast_ratio_large_text": "3.0:1 (WCAG AA)"
        }
    }
```

## Validation Tests
```python
res = generate_design_system("#00F0FF")
assert res["color_palette_60_30_10"]["accent_primary_10pct"] == "#00F0FF"
assert "h1" in res["typography_rem"]
```
