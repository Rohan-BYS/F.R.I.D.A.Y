---
name: ai_art_prompt_synthesizer
description: Synthesizes hyper-detailed image generation prompts with camera focal lengths, lighting setups, and aspect ratios.
category: design
version: 1.0.0
created_at: 2026-09-25 01:38:05
---

# 🧠 Learned Skill: ai_art_prompt_synthesizer

> Synthesizes hyper-detailed image generation prompts with camera focal lengths, lighting setups, and aspect ratios.

## Implementation Code
```python
def build_generative_art_prompt(subject: str, mood: str, camera_lens: str = "85mm f/1.4", lighting: str = "volumetric cinematic rim light", aspect_ratio: str = "16:9") -> dict:
    prompt = (
        f"A cinematic masterpiece of {subject}, {mood} atmosphere, "
        f"shot on Hasselblad H6D-100c with {camera_lens}, {lighting}, "
        f"photorealistic 8k, hyper-detailed textures, ray tracing reflections, Octane render --ar {aspect_ratio} --v 6.1"
    )
    return {
        "subject": subject,
        "constructed_prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "negative_prompt": "blurry, low quality, distorted anatomy, duplicate fingers, oversaturated, watermark, signature"
    }
```

## Validation Tests
```python
res = build_generative_art_prompt("Iron Man helmet in high tech laboratory", "futuristic cybernetic")
assert "--ar 16:9" in res["constructed_prompt"]
assert "negative_prompt" in res
```
