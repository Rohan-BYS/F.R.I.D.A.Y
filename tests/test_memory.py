"""
Unit tests for Persistent Memory Engine (SQLite WAL + FTS5 Search).
"""

import tempfile
from pathlib import Path
import pytest
from friday_engine.llm.base import Role
from friday_engine.memory.memory_engine import PersistentMemoryEngine


def test_memory_wal_and_persistence():
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test_memory.db"

        # 1. Initialize engine
        engine = PersistentMemoryEngine(db_path=db_path)
        stats = engine.get_stats()
        assert stats["journal_mode"] == "WAL"

        # 2. Create session and add messages
        session_id = "test_session_1"
        engine.create_session(session_id=session_id, title="Unit Test Session")
        engine.add_message(session_id=session_id, role=Role.USER, content="Hello Friday, remember project Alpha")
        engine.add_message(session_id=session_id, role=Role.ASSISTANT, content="Acknowledged Rohan, project Alpha recorded.")

        # 3. Retrieve chronological messages
        messages = engine.get_messages(session_id=session_id)
        assert len(messages) == 2
        assert messages[0].content == "Hello Friday, remember project Alpha"
        assert messages[1].content == "Acknowledged Rohan, project Alpha recorded."

        # 4. Test FTS5 full-text search
        search_results = engine.search_memory("project Alpha")
        assert len(search_results) >= 1
        assert "project Alpha" in search_results[0].content

        engine.close()

        # 5. Re-open engine on same db_path (verify persistence across restart)
        engine_reopened = PersistentMemoryEngine(db_path=db_path)
        reopened_messages = engine_reopened.get_messages(session_id=session_id)
        assert len(reopened_messages) == 2
        assert reopened_messages[0].content == "Hello Friday, remember project Alpha"
        engine_reopened.close()
