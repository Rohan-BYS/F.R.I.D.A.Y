"""
F.R.I.D.A.Y. SQLite WAL Database Engine.
Reverse-engineered from Hermes state management (hermes_state_wal.py).
Provides crash-resilient, concurrent Write-Ahead Logging database transactions.
"""

from __future__ import annotations

import contextlib
import os
import sqlite3
import threading
from pathlib import Path
from typing import Generator, Optional
from friday_engine.logger import logger


class DatabaseConnectionPool:
    """
    Manages thread-local SQLite connections with WAL pragma enforcement.
    """

    def __init__(self, db_path: str | Path, busy_timeout_ms: int = 5000):
        self.db_path = Path(db_path)
        self.busy_timeout_ms = busy_timeout_ms
        self._local = threading.local()
        self._lock = threading.Lock()
        self._ensure_db_dir()
        self._initialize_pragmas()

    def _ensure_db_dir(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _create_raw_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            str(self.db_path),
            timeout=self.busy_timeout_ms / 1000.0,
            check_same_thread=False,
        )
        conn.row_factory = sqlite3.Row
        # Enable WAL mode and performance pragmas
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.execute(f"PRAGMA busy_timeout={self.busy_timeout_ms};")
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA cache_size=-64000;")  # 64 MB cache
        cursor.close()
        return conn

    def _initialize_pragmas(self) -> None:
        """Run once on startup to set WAL mode on the database file."""
        with self._lock:
            conn = self._create_raw_connection()
            try:
                row = conn.execute("PRAGMA journal_mode;").fetchone()
                mode = row[0].upper() if row else "UNKNOWN"
                logger.info(f"Initialized SQLite database at {self.db_path} with journal_mode={mode}")
            finally:
                conn.close()

    def get_connection(self) -> sqlite3.Connection:
        """Return thread-local connection."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = self._create_raw_connection()
        return self._local.conn

    @contextlib.contextmanager
    def transaction(self) -> Generator[sqlite3.Cursor, None, None]:
        """Context manager for write transactions with automated rollback on error."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

    @contextlib.contextmanager
    def readonly(self) -> Generator[sqlite3.Cursor, None, None]:
        """Context manager for read queries."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def close(self) -> None:
        """Close thread connection."""
        if hasattr(self._local, "conn") and self._local.conn:
            try:
                self._local.conn.close()
            except Exception:
                pass
            self._local.conn = None
