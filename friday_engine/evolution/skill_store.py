"""
F.R.I.D.A.Y. Skill Store.
Reverse-engineered from Hermes Self-Evolution (skill_module.py).
Persists learned skills in SQLite with FTS5 search and generates SKILL.md specs.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from friday_engine.logger import logger
from friday_engine.memory.sqlite_wal import DatabaseConnectionPool
from friday_engine.tool_forge.forge import ToolForge
from friday_engine.tool_forge.models import ToolDefinition


class SkillStore:
    """
    Manages persistent learned skills, SKILL.md exports, and ToolForge integration.
    """

    def __init__(
        self,
        pool: DatabaseConnectionPool,
        skills_dir: str | Path = "data/skills",
        forge: Optional[ToolForge] = None,
    ):
        self.pool = pool
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.forge = forge

    def save_skill(
        self,
        name: str,
        description: str,
        code: str,
        test_code: Optional[str] = None,
        category: str = "general",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Save skill to SQLite database and write SKILL.md file.
        Also loads into ToolForge if active.
        """
        now = time.time()
        meta_json = json.dumps(metadata or {})
        clean_name = name.strip().lower().replace(" ", "_")

        # 1. Save to SQLite
        with self.pool.transaction() as cur:
            cur.execute(
                """
                INSERT INTO skills (name, description, category, version, code, test_code, metadata_json, created_at, updated_at)
                VALUES (?, ?, ?, '1.0.0', ?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    description = excluded.description,
                    code = excluded.code,
                    test_code = excluded.test_code,
                    metadata_json = excluded.metadata_json,
                    updated_at = excluded.updated_at;
                """,
                (clean_name, description, category, code, test_code or "", meta_json, now, now),
            )

        # 2. Write to SKILL.md file (Hermes / Antigravity format)
        skill_folder = self.skills_dir / clean_name
        skill_folder.mkdir(parents=True, exist_ok=True)
        skill_file = skill_folder / "SKILL.md"

        skill_md_content = f"""---
name: {clean_name}
description: {description}
category: {category}
version: 1.0.0
created_at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))}
---

# 🧠 Learned Skill: {clean_name}

> {description}

## Implementation Code
```python
{code.strip()}
```

## Validation Tests
```python
{(test_code or '').strip()}
```
"""
        skill_file.write_text(skill_md_content, encoding="utf-8")
        logger.info(f"Skill '{clean_name}' saved to database and wrote {skill_file}")

        # 3. Hot-load into ToolForge if available
        if self.forge:
            tool_def = ToolDefinition(
                name=clean_name,
                description=description,
                code=code,
                test_code=test_code,
            )
            try:
                self.forge.synthesize_tool(tool_def)
                logger.info(f"Skill '{clean_name}' successfully hot-loaded into active ToolForge runtime.")
            except Exception as exc:
                logger.warning(f"Skill '{clean_name}' saved, but ToolForge hot-load failed: {exc}")

        return True

    def get_skill(self, name: str) -> Optional[Dict[str, Any]]:
        """Retrieve skill record by name."""
        clean_name = name.strip().lower().replace(" ", "_")
        with self.pool.readonly() as cur:
            cur.execute(
                """
                SELECT name, description, category, version, code, test_code, metadata_json, created_at, updated_at
                FROM skills WHERE name = ?;
                """,
                (clean_name,),
            )
            row = cur.fetchone()
            if not row:
                return None
            return {
                "name": row["name"],
                "description": row["description"],
                "category": row["category"],
                "version": row["version"],
                "code": row["code"],
                "test_code": row["test_code"],
                "metadata": json.loads(row["metadata_json"] or "{}"),
                "created_at": row["created_at"],
            }

    def search_skills(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search skills using FTS5 index."""
        cleaned_query = query.replace("'", "''").replace('"', '""').strip()
        if not cleaned_query:
            return []

        fts_query = f"{cleaned_query}*"
        with self.pool.readonly() as cur:
            try:
                cur.execute(
                    """
                    SELECT s.name, s.description, s.category, s.code, skills_fts.rank
                    FROM skills_fts
                    JOIN skills s ON s.rowid = skills_fts.rowid
                    WHERE skills_fts MATCH ?
                    ORDER BY rank LIMIT ?;
                    """,
                    (fts_query, limit),
                )
                rows = cur.fetchall()
                return [{"name": r["name"], "description": r["description"], "category": r["category"], "code": r["code"]} for r in rows]
            except Exception as exc:
                logger.warning(f"Skills FTS query failed: {exc}")
                return []

    def list_all_skills(self) -> List[str]:
        """List all skill names."""
        with self.pool.readonly() as cur:
            cur.execute("SELECT name FROM skills ORDER BY name ASC;")
            return [r["name"] for r in cur.fetchall()]
