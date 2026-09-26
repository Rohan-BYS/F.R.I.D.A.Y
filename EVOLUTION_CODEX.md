# F.R.I.D.A.Y. Evolution Codex 🧬

**Purpose:** This codex is the living brain-dump of F.R.I.D.A.Y.'s learning process.
As F.R.I.D.A.Y. encounters new technologies, builds new tools, and faces errors,
she documents the *perfected methodology* here.

When `friday-evolve.py` is executed, this codex is injected directly into the
"Child Version" so it inherits all wisdom without repeating the failures.

**Total Learnings:** 0
**Last Updated:** Initial creation

---

## Format for New Learnings:

### [Technology / Skill Name]
* **Date:** YYYY-MM-DD
* **The Hurdle:** What went wrong during the initial attempt?
* **The Solution:** How was it bypassed or fixed?
* **The Perfected Method:** The exact working steps, dependencies, or code logic
  that the Child Version should use from Day 1.
* **Dependencies:** `package1, package2`

```python
# Optional: The perfected code snippet
```

---

## How F.R.I.D.A.Y. Should Use This

When F.R.I.D.A.Y. encounters a problem and solves it, she should call:

```python
from friday_engine.evolution.distiller import SkillDistiller
# Or directly via the evolution engine:
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from friday_evolve import EvolutionCodex

codex = EvolutionCodex()
codex.log_learning(
    category="browser_automation",
    skill_name="Gmail IMAP Login",
    hurdle="Google blocks browser automation with Captcha",
    solution="Use IMAP with App Passwords instead of Playwright",
    perfected_method="1. Enable 2FA on Gmail. 2. Generate App Password. 3. Connect via imaplib with App Password.",
    code_snippet="import imaplib\nmail = imaplib.IMAP4_SSL('imap.gmail.com')\nmail.login('friday@gmail.com', 'app-password-here')",
    dependencies=["imaplib"]
)
```

---

## Logged Evolutions

*(F.R.I.D.A.Y. will append new learnings below this line autonomously)*
