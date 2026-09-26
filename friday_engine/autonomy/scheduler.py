"""
F.R.I.D.A.Y. Proactive Agency (The Phantom Scheduler).
Allows F.R.I.D.A.Y. to wake up and execute tasks without human prompting.
"""

from typing import Any, Callable, Dict, Optional
from friday_engine.logger import logger

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.triggers.interval import IntervalTrigger
    from apscheduler.triggers.date import DateTrigger
    SCHEDULER_AVAILABLE = True
except ImportError:
    SCHEDULER_AVAILABLE = False


class ProactiveScheduler:
    """
    Manages background tasks that give F.R.I.D.A.Y. proactive agency.
    """
    def __init__(self, engine: Any = None):
        self.engine = engine
        self.scheduler = AsyncIOScheduler() if SCHEDULER_AVAILABLE else None
        self.jobs: Dict[str, Any] = {}

    def start(self):
        if not SCHEDULER_AVAILABLE:
            logger.error("APScheduler not installed. Proactive Agency disabled.")
            return
        
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Phantom Scheduler online. F.R.I.D.A.Y. now has proactive agency.")

    def shutdown(self):
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown()

    def schedule_cron(self, job_id: str, func: Callable, cron_expr: str, **kwargs):
        """Schedule a task using a cron expression (e.g. '0 8 * * *' for 8 AM daily)."""
        if not self.scheduler: return
        try:
            job = self.scheduler.add_job(
                func,
                CronTrigger.from_crontab(cron_expr),
                id=job_id,
                replace_existing=True,
                kwargs=kwargs
            )
            self.jobs[job_id] = job
            logger.info(f"Proactive job '{job_id}' scheduled with cron: {cron_expr}")
        except Exception as e:
            logger.error(f"Failed to schedule cron job {job_id}: {e}")

    def schedule_interval(self, job_id: str, func: Callable, minutes: int, **kwargs):
        """Schedule a task to run every X minutes."""
        if not self.scheduler: return
        try:
            job = self.scheduler.add_job(
                func,
                IntervalTrigger(minutes=minutes),
                id=job_id,
                replace_existing=True,
                kwargs=kwargs
            )
            self.jobs[job_id] = job
            logger.info(f"Proactive job '{job_id}' scheduled every {minutes} minutes.")
        except Exception as e:
            logger.error(f"Failed to schedule interval job {job_id}: {e}")

    def remove_job(self, job_id: str):
        if not self.scheduler: return
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
            del self.jobs[job_id]
            logger.info(f"Proactive job '{job_id}' removed.")
