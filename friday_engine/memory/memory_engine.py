"""
F.R.I.D.A.Y. Persistent Memory Engine.
Replaces volatile in-memory sessions with SQLite WAL + FTS5 full-text indexing.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from friday_engine.llm.base import LLMMessage, Role
from friday_engine.logger import logger
from friday_engine.memory.fts_index import ensure_fts_schema, search_messages_fts
from friday_engine.memory.models import (
    MemorySearchResult,
    MessageRecord,
    MessageRole,
    SessionRecord,
)
from friday_engine.memory.sqlite_wal import DatabaseConnectionPool


class PersistentMemoryEngine:
    """
    Persistent memory engine providing sub-millisecond keyword/semantic search,
    atomic transactions, and conversation recall.
    """

    def __init__(self, db_path: str | Path = "data/friday_state.db"):
        self.db_path = Path(db_path)
        self.pool = DatabaseConnectionPool(self.db_path)
        self._init_database()

    def _init_database(self) -> None:
        """Ensure schemas and triggers are loaded."""
        conn = self.pool.get_connection()
        ensure_fts_schema(conn)

    def create_session(self, session_id: str, title: str = "Active Session", metadata: Optional[Dict[str, Any]] = None) -> SessionRecord:
        """Create or initialize a session."""
        now = time.time()
        meta_json = json.dumps(metadata or {})
        with self.pool.transaction() as cur:
            cur.execute(
                """
                INSERT INTO sessions (session_id, title, created_at, updated_at, is_archived, metadata_json)
                VALUES (?, ?, ?, ?, 0, ?)
                ON CONFLICT(session_id) DO UPDATE SET updated_at = excluded.updated_at;
                """,
                (session_id, title, now, now, meta_json),
            )
        return SessionRecord(session_id=session_id, title=title, created_at=now, updated_at=now, metadata=metadata or {})

    def add_message(
        self,
        session_id: str,
        role: MessageRole | Role | str,
        content: str,
        tool_name: Optional[str] = None,
        tool_calls: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MessageRecord:
        """Persist a message into the database. FTS5 trigger runs automatically."""
        # Ensure session exists
        self.create_session(session_id=session_id)

        role_str = role.value if hasattr(role, "value") else str(role)
        now = time.time()
        meta_json = json.dumps(metadata) if metadata else None

        with self.pool.transaction() as cur:
            cur.execute(
                """
                INSERT INTO messages (session_id, role, content, tool_name, tool_calls, metadata_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (session_id, role_str, content, tool_name, tool_calls, meta_json, now),
            )
            msg_id = cur.lastrowid

            # Update session timestamp
            cur.execute("UPDATE sessions SET updated_at = ? WHERE session_id = ?;", (now, session_id))

        return MessageRecord(
            id=msg_id,
            session_id=session_id,
            role=role_str,
            content=content,
            tool_name=tool_name,
            tool_calls=tool_calls,
            created_at=now,
        )

    def get_messages(self, session_id: str, limit: int = 50) -> List[LLMMessage]:
        """Fetch chronological message history formatted for LLMRouter."""
        with self.pool.readonly() as cur:
            cur.execute(
                """
                SELECT role, content FROM (
                    SELECT id, role, content
                    FROM messages
                    WHERE session_id = ?
                    ORDER BY id DESC
                    LIMIT ?
                ) ORDER BY id ASC;
                """,
                (session_id, limit),
            )
            rows = cur.fetchall()

        messages = []
        for r in rows:
            messages.append(LLMMessage(role=Role(r["role"]) if r["role"] in Role._value2member_map_ else r["role"], content=r["content"]))
        return messages

    def search_memory(self, query: str, session_id: Optional[str] = None, limit: int = 10) -> List[MemorySearchResult]:
        """Search across all past memories and conversations using FTS5."""
        conn = self.pool.get_connection()
        return search_messages_fts(conn, query=query, session_id=session_id, limit=limit)

    def get_stats(self) -> Dict[str, Any]:
        """Return memory engine metrics."""
        with self.pool.readonly() as cur:
            cur.execute("SELECT COUNT(*) FROM sessions;")
            session_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM messages;")
            message_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM skills;")
            skills_count = cur.fetchone()[0]

        file_size_bytes = self.db_path.stat().st_size if self.db_path.exists() else 0

        return {
            "db_path": str(self.db_path),
            "total_sessions": session_count,
            "total_messages": message_count,
            "total_skills": skills_count,
            "db_size_kb": round(file_size_bytes / 1024, 2),
            "journal_mode": "WAL",
        }

    def close(self) -> None:
        self.pool.close()
