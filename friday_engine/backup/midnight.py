"""
F.R.I.D.A.Y. Midnight Protocol.
Law 3 of Friday: The Law of Immortality.
Automated repository synchronization, self-backup, and disaster recovery.
"""

from __future__ import annotations

import datetime
import subprocess
from pathlib import Path
from typing import Dict, Optional, Tuple
from friday_engine.config import MidnightProtocolConfig
from friday_engine.logger import logger


class MidnightProtocol:
    """
    Orchestrates the Midnight Protocol git sync and backup operations.
    """

    def __init__(
        self,
        config: Optional[MidnightProtocolConfig] = None,
        repo_dir: Optional[Path | str] = None,
    ):
        self.config = config or MidnightProtocolConfig()
        self.repo_dir = Path(repo_dir) if repo_dir else Path.cwd()

    def _run_git_cmd(self, args: list[str]) -> Tuple[int, str, str]:
        """Execute a git command in the repository directory."""
        proc = subprocess.run(
            ["git"] + args,
            cwd=str(self.repo_dir),
            capture_output=True,
            text=True,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()

    def check_git_status(self) -> Dict[str, Any]:
        """Check status of repository."""
        code, out, err = self._run_git_cmd(["status", "--porcelain"])
        has_changes = bool(out)
        return {
            "is_git_repo": code == 0,
            "has_uncommitted_changes": has_changes,
            "changed_files_count": len(out.splitlines()) if out else 0,
            "raw_status": out,
            "error": err if code != 0 else None,
        }

    async def run_immortality_loop(self, memory_engine: Any):
        """
        Phase 5: The Immortality Loop.
        Continuously checks the time and triggers Midnight Protocol at the scheduled time.
        """
        import asyncio
        if not self.config.enabled:
            logger.info("Immortality Loop disabled.")
            return

        logger.info(f"Immortality Loop started. Scheduled for {self.config.schedule_time} daily.")
        
        while True:
            now = datetime.datetime.now()
            schedule_hour, schedule_minute = map(int, self.config.schedule_time.split(':'))
            
            # If it's the exact minute, run the backup
            if now.hour == schedule_hour and now.minute == schedule_minute:
                self.execute_backup(memory_engine=memory_engine)
                # Sleep for 61 seconds to avoid triggering twice in the same minute
                await asyncio.sleep(61)
            else:
                # Check every 30 seconds
                await asyncio.sleep(30)

    def execute_backup(self, memory_engine: Optional[Any] = None, custom_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute full backup cycle:
        1. Export memory to JSON
        2. git add -A
        3. git commit -m "[Midnight Protocol] Nightly backup YYYY-MM-DD"
        4. git push origin <branch> (if remote configured)
        """
        if not self.config.enabled:
            logger.info("Midnight Protocol is disabled in configuration. Skipping.")
            return {"status": "skipped", "reason": "disabled"}

        logger.info("=== [MIDNIGHT PROTOCOL INITIATED] Immortality Routine Triggered ===")
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = custom_message or f"{self.config.commit_message_prefix} - {date_str}"

        # 0. Export Memory to git-trackable format
        if memory_engine:
            try:
                import json
                export_path = Path("data/memory_snapshot.json")
                export_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Fetch recent important context to backup
                snapshot = memory_engine.get_messages(session_id="default_session", limit=1000)
                formatted = [{"role": msg.role.value if hasattr(msg.role, 'value') else msg.role, "content": msg.content} for msg in snapshot]
                
                export_path.write_text(json.dumps(formatted, indent=2), encoding="utf-8")
                logger.info(f"Memory snapshot exported to {export_path}")
            except Exception as e:
                logger.error(f"Failed to export memory: {e}")

        # 1. Stage all changes
        code, out, err = self._run_git_cmd(["add", "-A"])
        if code != 0:
            logger.error(f"Git add failed: {err}")
            return {"status": "failed", "step": "git add", "error": err}

        # 2. Check if there are changes to commit
        code, out, _ = self._run_git_cmd(["status", "--porcelain"])
        if not out:
            logger.info("No modifications detected. Codebase is clean and up to date.")
            return {"status": "success", "step": "clean", "message": "Nothing to commit."}

        # 3. Commit
        code, out, err = self._run_git_cmd(["commit", "-m", commit_msg])
        if code != 0:
            logger.error(f"Git commit failed: {err}")
            return {"status": "failed", "step": "git commit", "error": err}
        logger.info(f"Committed snapshot: {commit_msg}")

        # 4. Push if auto_push is enabled
        push_status = "skipped"
        if self.config.auto_push:
            remote = self.config.git_remote
            branch = self.config.git_branch
            code, out, err = self._run_git_cmd(["push", remote, branch])
            if code == 0:
                push_status = "pushed"
                logger.info(f"Successfully pushed state to {remote}/{branch}")
            else:
                push_status = "push_warning"
                logger.warning(f"Git push could not complete (remote may not be configured): {err}")

        logger.info("=== [MIDNIGHT PROTOCOL COMPLETED] Soul preserved. ===")
        return {
            "status": "success",
            "commit_message": commit_msg,
            "push_status": push_status,
            "timestamp": date_str,
        }
