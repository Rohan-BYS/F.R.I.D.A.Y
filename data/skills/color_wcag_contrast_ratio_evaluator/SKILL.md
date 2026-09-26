---
name: color_wcag_contrast_ratio_evaluator
description: Calculates relative luminance and exact contrast ratio between foreground and background colors (WCAG AA/AAA).
category: design
version: 1.0.0
created_at: 2026-09-25 01:38:08
---

# 🧠 Learned Skill: color_wcag_contrast_ratio_evaluator

> Calculates relative luminance and exact contrast ratio between foreground and background colors (WCAG AA/AAA).

## Implementation Code
```python
def evaluate_wcag_contrast(fg_hex: str, bg_hex: str) -> dict:
    def hex_to_luminance(h):
        h = h.lstrip("#")
        rgb = [int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
        linear = [(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4) for c in rgb]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    l1 = hex_to_luminance(fg_hex)
    l2 = hex_to_luminance(bg_hex)
    brightest = max(l1, l2)
    darkest = min(l1, l2)
    ratio = (brightest + 0.05) / (darkest + 0.05)
    return {
        "contrast_ratio": round(ratio, 2),
        "wcag_aa_normal_text_pass": ratio >= 4.5,
        "wcag_aa_large_text_pass": ratio >= 3.0,
        "wcag_aaa_normal_text_pass": ratio >= 7.0
    }
```

## Validation Tests
```python
res = evaluate_wcag_contrast("#FFFFFF", "#000000")
assert res["contrast_ratio"] == 21.0
assert res["wcag_aaa_normal_text_pass"] is True
```
