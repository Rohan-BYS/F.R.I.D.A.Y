"""
Full-Text Search (FTS5) & Relational Schema Setup.
Reverse-engineered from Hermes state FTS (hermes_state_fts.py).
Provides automated external-content virtual tables and sync triggers.
"""

from __future__ import annotations

import sqlite3
from typing import List, Optional
from friday_engine.logger import logger
from friday_engine.memory.models import MemorySearchResult

SCHEMA_DDL = """
-- 1. SESSIONS TABLE
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    is_archived INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT
);

-- 2. MESSAGES TABLE
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    tool_name TEXT,
    tool_calls TEXT,
    metadata_json TEXT,
    created_at REAL NOT NULL,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id, created_at);

-- 3. MESSAGES FTS5 VIRTUAL TABLE (Full-Text Search)
CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
    content,
    tool_name,
    tool_calls,
    content='messages',
    content_rowid='id',
    tokenize='porter unicode61'
);

-- 4. FTS TRIGGERS (Automated Sync between messages and messages_fts)
CREATE TRIGGER IF NOT EXISTS messages_ai AFTER INSERT ON messages BEGIN
    INSERT INTO messages_fts(rowid, content, tool_name, tool_calls)
    VALUES (new.id, new.content, new.tool_name, new.tool_calls);
END;

CREATE TRIGGER IF NOT EXISTS messages_ad AFTER DELETE ON messages BEGIN
    INSERT INTO messages_fts(messages_fts, rowid, content, tool_name, tool_calls)
    VALUES('delete', old.id, old.content, old.tool_name, old.tool_calls);
END;

CREATE TRIGGER IF NOT EXISTS messages_au AFTER UPDATE ON messages BEGIN
    INSERT INTO messages_fts(messages_fts, rowid, content, tool_name, tool_calls)
    VALUES('delete', old.id, old.content, old.tool_name, old.tool_calls);
    INSERT INTO messages_fts(rowid, content, tool_name, tool_calls)
    VALUES (new.id, new.content, new.tool_name, new.tool_calls);
END;

-- 5. SKILLS PERSISTENCE TABLE
CREATE TABLE IF NOT EXISTS skills (
    name TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'general',
    version TEXT NOT NULL DEFAULT '1.0.0',
    code TEXT NOT NULL,
    test_code TEXT,
    metadata_json TEXT,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL
);

-- 6. SKILLS FTS5 VIRTUAL TABLE
CREATE VIRTUAL TABLE IF NOT EXISTS skills_fts USING fts5(
    name,
    description,
    category,
    content='skills',
    content_rowid='rowid',
    tokenize='porter unicode61'
);

CREATE TRIGGER IF NOT EXISTS skills_ai AFTER INSERT ON skills BEGIN
    INSERT INTO skills_fts(rowid, name, description, category)
    VALUES (new.rowid, new.name, new.description, new.category);
END;

CREATE TRIGGER IF NOT EXISTS skills_ad AFTER DELETE ON skills BEGIN
    INSERT INTO skills_fts(skills_fts, rowid, name, description, category)
    VALUES('delete', old.rowid, old.name, old.description, old.category);
END;
"""


def ensure_fts_schema(conn: sqlite3.Connection) -> None:
    """Initialize database tables, views, and FTS triggers."""
    try:
        cursor = conn.cursor()
        cursor.executescript(SCHEMA_DDL)
        conn.commit()
        cursor.close()
        logger.info("Database relational schema and FTS5 triggers verified successfully.")
    except Exception as exc:
        logger.error(f"Failed to ensure FTS schema: {exc}", exc_info=True)
        raise


def search_messages_fts(
    conn: sqlite3.Connection,
    query: str,
    session_id: Optional[str] = None,
    limit: int = 10,
) -> List[MemorySearchResult]:
    """
    Search messages using SQLite FTS5 BM25 relevance ranking.
    """
    cleaned_query = query.replace("'", "''").replace('"', '""').strip()
    if not cleaned_query:
        return []

    # Sanitize FTS query for boolean tokens
    fts_match_query = f'"{cleaned_query}"' if " " in cleaned_query else f"{cleaned_query}*"

    sql = """
    SELECT
        m.id,
        m.session_id,
        m.role,
        m.content,
        snippet(messages_fts, 0, '<b>', '</b>', '...', 20) as snippet,
        messages_fts.rank,
        m.created_at
    FROM messages_fts
    JOIN messages m ON m.id = messages_fts.rowid
    WHERE messages_fts MATCH ?
    """
    params = [fts_match_query]

    if session_id:
        sql += " AND m.session_id = ? "
        params.append(session_id)

    sql += " ORDER BY rank LIMIT ?;"
    params.append(limit)

    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        results = []
        for r in rows:
            results.append(
                MemorySearchResult(
                    message_id=r["id"],
                    session_id=r["session_id"],
                    role=r["role"],
                    content=r["content"],
                    snippet=r["snippet"] or r["content"][:100],
                    rank=float(r["rank"]),
                    created_at=r["created_at"],
                )
            )
        return results
    except sqlite3.OperationalError as exc:
        logger.warning(f"FTS query error for '{query}': {exc}")
        return []
    finally:
        cursor.close()
